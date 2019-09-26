
class RSquareHighlighter:

    def __init__(self):
        pass

    def highlight_rsquare(self,x):
        style = []
        for v in x:
            if v < 0.33:
                style.append('background-color: red')
            elif v > 0.66:
                style.append('background-color: green')
            else:
                style.append('background-color: yellow')
        return style