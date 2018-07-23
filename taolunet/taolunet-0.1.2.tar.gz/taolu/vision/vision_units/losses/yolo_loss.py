import torch
import torch.nn.functional as F
from .loss import Loss


class YoloLoss(Loss):
    def __init__(self, cfg):
        super(YoloLoss, self).__init__(cfg)
        self.S = cfg['C']
        self.B = cfg['B']
        self.classes = cfg['num_classes']
        self.lambda_coobj = cfg['lambda_coobj']
        self.lambda_noobj = cfg['lambda_noobj']

    def compute_iou(self, box1, box2):
        # N==2, M==1?
        N = box1.size(0)
        M = box2.size(0)

        # choose the left top
        lt = torch.max(
            box1[:, :2].unsqueeze(1).expand(N, M, 2),  # [N,2] -> [N,1,2] -> [N,M,2]
            box2[:, :2].unsqueeze(0).expand(N, M, 2),  # [M,2] -> [1,M,2] -> [N,M,2]
        )
        rb = torch.min(
            box1[:, 2:].unsqueeze(1).expand(N, M, 2),  # [N,2] -> [N,1,2] -> [N,M,2]
            box2[:, 2:].unsqueeze(0).expand(N, M, 2),  # [M,2] -> [1,M,2] -> [N,M,2]
        )

        wh = rb - lt  # [N,M,2]
        wh[wh < 0] = 0  # clip at 0

        # The area of the intersect zone
        inter = wh[:, :, 0] * wh[:, :, 1]  # [N,M]

        # The area of box1
        area1 = (box1[:, 2] - box1[:, 0]) * (box1[:, 3] - box1[:, 1])  # [N,]
        # The area of box2
        area2 = (box2[:, 2] - box2[:, 0]) * (box2[:, 3] - box2[:, 1])  # [M,]
        area1 = area1.unsqueeze(1).expand_as(inter)  # [N,] -> [N,1] -> [N,M]
        area2 = area2.unsqueeze(0).expand_as(inter)  # [M,] -> [1,M] -> [N,M]
        iou = inter / (area1 + area2 - inter)
        return iou

    def forward(self, pred, gt):
        '''
        The ground truth boxes only penalize the corresponding pred cells (has obj penal).
        The ground truth no boxes only penalize the corresponding pred cells (has no obj penal)
        '''

        N = pred.size()[0]
        batch_size = pred.size()[0]
        pred = pred.view(N, self.S, self.S, self.B * 5 + self.classes)
        gt_has_obj_factors = (gt[:, :, :, 4] > 0).unsqueeze(-1).expand_as(gt)  # (batch,h,w, B*2+C)
        gt_no_obj_factors = (gt[:, :, :, 4] == 0).unsqueeze(-1).expand_as(gt)

        # This extracts all the cells corresponding with the gt has object cells. Also the batch is mixed in.
        has_obj_pred = pred[gt_has_obj_factors].view(-1, self.B * 5 + self.classes)  # has obj pred ()

        # Only obtain the x,y,w,h,confidence, # all the pred boxes corresponding with the ground truth boxes, batch?
        boxes_pred = has_obj_pred[:, :self.B * 5].contiguous().view(-1, 5)
        # only obtain the Classespred.size()
        classes_pred = has_obj_pred[:, self.B * 5:]

        has_obj_gt = gt[gt_has_obj_factors].view(-1, self.B * 5 + self.classes)

        # all the ground truth boxes also with the emply bounding boxes (x,y,w,h,C)
        boxes_gt = has_obj_gt[:, :self.B * 5].contiguous().view(-1, 5)
        classes_gt = has_obj_gt[:, self.B * 5:]

        # The last item in the yolo loss
        class_loss = F.mse_loss(classes_pred, classes_gt, size_average=False)

        # the pred boxes corresponding with the ground truth no object boxes.
        no_obj_pred = pred[gt_no_obj_factors].view(-1, self.B * 5 + self.classes)
        no_obj_gt = gt[gt_no_obj_factors].view(-1, self.B * 5 + self.classes)
        no_obj_multiplier = torch.zeros(no_obj_pred.size(), dtype=torch.uint8, device=no_obj_pred.device)

        # When the confidence is 1
        no_obj_multiplier[:, 4] = 1
        no_obj_multiplier[:, 9] = 1

        # Only extracts the pred cells confidences  which correspond with gt no obj boxes
        no_obj_pred_C = no_obj_pred[no_obj_multiplier]

        # Only extracts the pred cells confidences which correspond with gt no obj boxes
        no_obj_gt_C = no_obj_gt[no_obj_multiplier]

        # Penalize the no object Confidence
        noo_obj_C_loss = F.mse_loss(no_obj_pred_C, no_obj_gt_C, size_average=False)

        has_obj_resp_multiplier = torch.zeros(boxes_gt.size(), dtype=torch.uint8, device=boxes_gt.device)
        has_obj_no_resp_multiplier = torch.zeros(boxes_gt.size(), dtype=torch.uint8, device=boxes_gt.device)
        for i in range(0, boxes_gt.size()[0], self.B):
            # choose the corresponding pred cell two boxes
            pred_box = boxes_pred[i:i + self.B]
            pred_box_coords = torch.autograd.Variable(torch.FloatTensor(pred_box.size()))

            # normalize the coords, (x,y,w,h) -> (left_top_x, left_top_y, right_bottom_x, right_bottom_y)
            pred_box_coords[:, :2] = pred_box[:, :2] - 0.5 * pred_box[:, 2:4]
            pred_box_coords[:, 2:4] = pred_box[:, :2] + 0.5 * pred_box[:, 2:4]
            gt_box = boxes_gt[i].view(-1, 5)

            gt_box_coords = torch.autograd.Variable(torch.FloatTensor(gt_box.size()))
            gt_box_coords[:, :2] = gt_box[:, :2] - 0.5 * gt_box[:, 2:4]
            gt_box_coords[:, 2:4] = gt_box[:, :2] + 0.5 * gt_box[:, 2:4]

            # compute the iou of two boxes of pred and one boxes of gt to check which box of the pred is choosed to response to the gt
            # the
            iou = self.compute_iou(pred_box_coords[:, :4], gt_box_coords[:, :4])
            max_iou, max_index = iou.max(0)
            max_index = max_index.data
            has_obj_resp_multiplier[i + max_index] = 1
            has_obj_no_resp_multiplier[i + 1 - max_index] = 1

        boxes_pred_response = boxes_pred[has_obj_resp_multiplier].view(-1, 5)
        boxes_gt_response = boxes_gt[has_obj_resp_multiplier].view(-1, 5)
        contain_loss = F.mse_loss(boxes_pred_response[:, 4], boxes_gt_response[:, 4], size_average=False)
        loc_loss = F.mse_loss(boxes_pred_response[:, :2], boxes_gt_response[:, :2], size_average=False) + F.mse_loss(
            boxes_pred_response[:, 2:4], boxes_gt_response[:, 2:4], size_average=False)

        boxes_pred_not_response = boxes_pred[has_obj_no_resp_multiplier].view(-1, 5)
        boxes_gt_not_response = boxes_gt[has_obj_no_resp_multiplier].view(-1, 5)
        boxes_gt_not_response[:, 4] = 0
        not_contain_loss = F.mse_loss(boxes_pred_not_response[:, 4], boxes_gt_not_response[:, 4], size_average=False)

        return (
                       self.lambda_coobj * loc_loss + contain_loss + not_contain_loss + self.lambda_noobj * noo_obj_C_loss + class_loss) / N
