from jinja2 import Environment, BaseLoader
from weasyprint import HTML
import tempfile
import matplotlib.pyplot as plt
from collections import OrderedDict
from section import Section
import os
import pkg_resources
eps = .000001

def F1_score(prec, rec):
    return 2 * (prec * rec) / (prec + rec+eps)

class ReportML:
    def __init__(self,title, outputs=None):
        exists = pkg_resources.resource_exists(__name__, "templates/report.html")
        print(exists)
        temp = pkg_resources.resource_string(__name__, "templates/report.html")
        self.template = Environment(loader=BaseLoader).from_string(temp)
        self.pdf_params = {"title":title, "sections":[],"plots":[]}
        self.stats = None
        if outputs is not None:
            preds, truths = outputs
            self.stats = self.get_stats(preds, truths)
            section = Section("Stats", self.stats)
            self.add_section(section)
        self.plots_dir = tempfile.mkdtemp("plots")

    def render(self, path):
        out = self.template.render(self.pdf_params)
        print(out)
        HTML(string=out,base_url=self.plots_dir).write_pdf(path)

    def add_section(self,section):
        self.pdf_params["sections"].append(section)

    def get_stats(self,preds, true_labels):
        tp = 0.0
        fn = 0.0
        tn = 0.0
        fp = 0.0
        for (idx, pred) in enumerate(preds):
            truth = true_labels[idx]
            if truth == pred:
                if truth == 1:
                    tp += 1
                else:
                    tn += 1
            elif truth == 0:
                fp += 1
            else:
                fn += 1
        precision = tp / (tp + fp+eps)
        recall = tp / (tp + fn+eps)
        acc = (tp + tn) / (tp + tn + fp + fn+eps)
        tnr = tn / (tn + fp+eps)
        F1 = F1_score(precision, recall)
        return OrderedDict([("F1", F1),
                            ("Precision", precision),
                            ("Recall",recall),
                            ("Accuracy", acc),
                            ("True Negative Rate",tnr),
                            ("|Examples|", len(preds)),
                            ("True Positives",tp),
                            ("False Positive",fp),
                            ("True Negatives",tn),
                            ("False Negatives",fn)])

    def add_plot(self, plot):
        """
        add a plot to the report
        :param plot: a plot object
        :return: None
        """
        fig = plot.plt_obj
        fig.savefig("{}/{}.png".format(self.plots_dir,plot.title),bbox_inches='tight')
        plot.path = "{}/{}.png".format(self.plots_dir,plot.title)
        self.pdf_params["plots"].append(plot)
        # now clear the matplotlib instance
        plt.clf()

