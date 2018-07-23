from taolu.demo.demo_base import DemoBase
import pickle

if __name__ == '__main__':
    demo = DemoBase("../vision/base_nets/yolov1.json", "object_detection")
    demo.go()
