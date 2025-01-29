import yaml


file_path = "/workspaces/hive-builder-template/.hive/private/Vagrantfile"
"""
特定のファイルの `ENV` という文字列を `vars` という文字列に置き換えます。

Args:
file_path: 置き換えたいファイルのパス
"""
with open(file_path, 'r') as f:
    file_content = f.read()
    file_content = file_content.replace('ENV', 'vars')
with open(file_path, 'w') as f:
    f.write(file_content)



def add_proxy_settings(yaml_file):
  """
  YAMLファイルにプロキシ設定を追加します。

  Args:
    yaml_file: 設定を追加するYAMLファイルのパス。
  """

  try:
    with open(yaml_file, 'r') as f:
      data = yaml.safe_load(f) or {}  # ファイルが存在しない場合は空の辞書を返す
  except FileNotFoundError:
    data = {}

  # プロキシ設定を追加
  data['HTTP_PROXY'] = "http://192.168.121.1:3128"
  data['HTTPS_PROXY'] = "http://192.168.121.1:3128"
  data['NO_PROXY'] = "p-hive0.test,p-hive1.test,p-hive2.test,localhost,127.0.0.1"

  with open(yaml_file, 'w') as f:
    yaml.safe_dump(data, f, indent=2)

# YAMLファイルのパスを指定して関数を呼び出す
yaml_file_path = '/workspaces/hive-builder-template/.hive/private/vagrant_vars.yml'  # ここにYAMLファイルのパスを入力してください
add_proxy_settings(yaml_file_path)