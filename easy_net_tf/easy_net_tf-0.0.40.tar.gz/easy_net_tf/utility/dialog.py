import tkinter
import tkinter.filedialog


class UtilityDialog:
    @staticmethod
    def tk_avoid(func, hint='', initial_dir='', mode=None):
        r = tkinter.Tk()
        r.withdraw()

        if mode is None:
            result = func(title=hint,
                          initialdir=initial_dir)
        else:
            result = func(mode=mode,
                          title=hint,
                          initial_dir=initial_dir)

        return result


if __name__ == '__main__':
    path = UtilityDialog.tk_avoid(func=tkinter.filedialog.askdirectory,
                                  hint='hello')
    print(path)
