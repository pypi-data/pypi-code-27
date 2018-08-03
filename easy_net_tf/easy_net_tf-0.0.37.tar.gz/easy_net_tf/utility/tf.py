import tensorflow as tf


class UtilityTf:
    @staticmethod
    def latest_checkpoint(model_dir=None, initial_dir=''):
        if model_dir is None:
            import tkinter
            import tkinter.filedialog

            r = tkinter.Tk()
            r.withdraw()
            model_dir = tkinter.filedialog.askdirectory(initialdir=initial_dir)
            if type(model_dir) == tuple:
                model_dir = ''

        return tf.train.latest_checkpoint(model_dir)


if __name__ == '__main__':
    path = UtilityTf.latest_checkpoint()

    print(path)
