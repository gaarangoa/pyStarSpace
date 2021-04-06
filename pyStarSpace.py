import subprocess
import logging

log = logging.getLogger()


class Starspace():
    def __init__(self, model_name='', items=10):
        self.model_name = model_name
        self.items = items+1

    def load(self):
        self.model = subprocess.Popen(
            ['query_predict', self.model_name, str(self.items)],
            shell=False,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            bufsize=0
        )

        for _ in range(28):
            log.info(self.model.stdout.readline())

    def parse_out(self, pred):

        label = str(pred).split('__label__')[1].strip().split()[0]
        prob = str(pred).split('[')[1].split(']')[0]
        return {"label": label, "score": float(prob)*100}

    def predict(self, input_string='', items=5):
        self.model.stdin.write(str.encode(input_string))
        preds = []
        for _ in range(self.items):
            pred = self.model.stdout.readline()
            try:
                preds.append(
                    self.parse_out(pred)
                )
            except:
                log.error(('prediction: ', pred))

        log.debug(('in the list: ', len(preds)))
        return sorted(preds, key=lambda x: x['score'], reverse=True)[1:items+1]
