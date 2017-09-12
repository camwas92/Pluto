from pathlib import Path



def collect_paths():
    basePath = Path(__file__).parents[2]  # get base path
    paths = {'Base': basePath, 'Input': (basePath / 'Input'), 'Output': (basePath / 'Output')}
    data = Path(__file__).parents[3]
    paths['Source_Data'] = data/'Data'
    return paths

