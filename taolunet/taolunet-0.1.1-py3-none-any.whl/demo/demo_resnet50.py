from taolu.demo.demo_base import DemoBase

if __name__ == '__main__':
    demo = DemoBase("../vision/base_nets/resnet50.json", "classification")
    demo.go()
