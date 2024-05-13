import yaml

# 读取配置文件
def read_config(filename):
    with open(filename, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            print(exc)

