import json
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from freqtrade import main

file_path = os.path.abspath(__file__)
folder_path = os.path.dirname(file_path)
user_data_path = os.path.join(folder_path, "user_data")
config_file = os.path.join(user_data_path, "config.json")
pair_config_file = os.path.join(user_data_path, "pair.json")
download_config_path = os.path.join(user_data_path, "download.json")

data_path = os.path.join(user_data_path, "data")
backtest_path = os.path.join(user_data_path, "backtest_results")
# hyperopt_result_path = os.path.join(user_data_path, "hyperopt_results")

# hyper_path = os.path.join(user_data_path, "data\\hyperliquid\\futures")

config: dict = {}


def move_folder_contents(source_folder, destination_folder):
    for filename in os.listdir(source_folder):
        src_file = os.path.join(source_folder, filename)
        dst_file = os.path.join(destination_folder, filename)
        shutil.move(src_file, dst_file)
        print(f"Moved {src_file} to {dst_file}")
    return


def timerange(day: int = 30):
    end_date = datetime.now() - timedelta(days=1)
    start_date = end_date - timedelta(days=day)
    return f"{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}"


def read_config(config_path: Path):
    with open(config_path, "r") as file:
        conf: dict = json.load(file)
    return conf


def write_config(conf: dict, config_path: Path):
    with open(config_path, "w") as file:
        json.dump(conf, file, indent=4)
    return


def del_folder_content(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            shutil.rmtree(dir_path)
    return


def edge(s: str, d: int = 30):
    time_range = timerange(day=d)
    return [
        "edge",
        "-c",
        config_file,
        "--userdir",
        user_data_path,
        "-s",
        s,
        "--timerange",
        time_range,
    ]


def install_ui():
    # args = ['install-ui' , '--erase']
    # args = ['install-ui' , '--ui-version' , '1.3.2']
    # args = ['install-ui' , '--help']
    args = ["install-ui"]
    return args


def backtesting_show():
    return ["backtesting-show", "-c", download_config_path, "--userdir", user_data_path]


def backtest_analize(d: int = 30):
    time_range = timerange(day=d)
    return [
        "backtesting-analysis",
        "-c",
        download_config_path,
        "--userdir",
        user_data_path,
        "--timerange",
        time_range,
    ]


def hyperopt_show(e: int = None):  # type: ignore
    if e is not None:
        return [
            "hyperopt-show",
            "-c",
            download_config_path,
            "--userdir",
            user_data_path,
            "-n",
            str(e),
        ]

    if e is None:
        return [
            "hyperopt-show",
            "-c",
            download_config_path,
            "--userdir",
            user_data_path,
        ]


def plot_profit(s: str, d: int = 10):
    time_range = timerange(day=d)
    return [
        "plot-profit",
        "-c",
        download_config_path,
        "--userdir",
        user_data_path,
        "--timerange",
        time_range,
        "-s",
        s,
    ]


def hyperopt_list():
    return ["hyperopt-list", "-c", download_config_path, "--userdir", user_data_path]


def strategy_update():
    return ["strategy-updater", "-c", config_file, "--userdir", user_data_path]


def webserver():
    return ["webserver", "-c", config_file, "--userdir", user_data_path]


def trade(s: str):
    args = ["trade", "-c", config_file, "--userdir", user_data_path, "-s", s]
    return args


def list_strategies():
    return ["list-strategies", "-c", config_file, "--userdir", user_data_path]


def new_strategy(s: str = None, t: str = "full"):  # type: ignore
    """
    full
    minimal
    advanced
    """
    return ["new-strategy", "--userdir", user_data_path, "--template", t, "-s", s]


def del_backtest_results():
    del_folder_content(backtest_path)
    print("deleted all content of backtest folder")
    return


# def del_hyperopt_result():
#     del_folder_content(hyperopt_result_path)
#     print("deleted all content of hyperopt result folder")
#     return


def del_downloaded_data():
    for root, dirs, files in os.walk(data_path, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            shutil.rmtree(dir_path)
    print("Deleted all content of data folder")
    return


def test_pairlist():
    return [
        "test-pairlist",
        "-c",
        config_file,
        "--userdir",
        user_data_path,
        "--one-column",
    ]


def plot_dataframe(s: str = None, p: str = None, d: int = 5):  # type: ignore
    time_range = timerange(day=d)
    return [
        "plot-dataframe",
        "-c",
        download_config_path,
        "--userdir",
        user_data_path,
        "-s",
        s,
        "-p",
        p,
        "--timerange",
        time_range,
    ]


def download_data(d: int = 35, tf: str = "5m"):
    time_range = timerange(day=d)
    return [
        "download-data",
        "-c",
        config_file,
        "--userdir",
        user_data_path,
        "--timerange",
        time_range,
        "-t",
        tf,
        "--erase",
    ]


def look_ahead(s: str, d: int = 30):
    time_range = timerange(day=d)
    return [
        "lookahead-analysis",
        "-c",
        download_config_path,
        "--userdir",
        user_data_path,
        "-s",
        s,
        "--timerange",
        time_range,
    ]


def resourcive_analyze(s: str, d: int = 30):
    time_range = timerange(day=d)
    return [
        "recursive-analysis",
        "-c",
        download_config_path,
        "--userdir",
        user_data_path,
        "-s",
        s,
        "--timerange",
        time_range,
    ]


def backtest(s: str = None, d: int = 10, use_time_detail: bool = False):  # type: ignore
    time_range = timerange(day=d)
    # if use_time_detail:
    #     return ['backtesting' , '-c',download_config_path,'--userdir',user_data_path , '--timerange', time_range ,'-s' , s , '--timeframe-detail' , '1m']

    return [
        "backtesting",
        "-c",
        config_file,
        "--userdir",
        user_data_path,
        "--timerange",
        time_range,
        "-s",
        s,
    ]


def hyperopt(
    s: str = None,  # type: ignore
    loss: str = "OnlyProfitHyperOptLoss",
    e: int = 150,
    d: int = 20,
    j: int = 11,
    use_detail_time: bool = False,
    spaces: list = ["buy", "sell", "roi", "stoploss"],
):  # type: ignore
    """
    ShortTradeDurHyperOptLoss
    OnlyProfitHyperOptLoss
    SharpeHyperOptLoss
    CalmarHyperOptLoss
    # MaxDrawDownHyperOptLoss
    MaxDrawDownRelativeHyperOptLoss
    SharpeHyperOptLossDaily
    SortinoHyperOptLoss
    SortinoHyperOptLossDaily
    ProfitDrawDownHyperOptLoss
     '--ignore-missing-spaces'
     ,'--analyze-per-epoch'
      ,'--disable-param-export'
      'trailing'
      'protection'
      --timeframe-detail
      '
      ,'--print-all'
    """
    time_range = timerange(day=d)
    if use_detail_time:
        return (
            [
                "hyperopt",
                "-c",
                download_config_path,
                "--userdir",
                user_data_path,
                "-s",
                s,
                "--timeframe-detail",
                "1m",
                "--spaces",
            ]
            + spaces
            + [
                "--hyperopt-loss",
                loss,
                "-e",
                str(e),
                "--timerange",
                time_range,
                "--ignore-missing-spaces",
                "--disable-param-export",
            ]
        )

    return (
        [
            "hyperopt",
            "-c",
            download_config_path,
            "--userdir",
            user_data_path,
            "-s",
            s,
            "--spaces",
        ]
        + spaces
        + [
            "--hyperopt-loss",
            loss,
            "-e",
            str(e),
            "--timerange",
            time_range,
            "--ignore-missing-spaces",
            "--disable-param-export",
        ]
    )


def create_userdir():
    return ["create-userdir", "--userdir", user_data_path]


#! backtest analyze
# main.main(backtest_analize(30))

#! create user dir
# main.main(create_userdir())

#! hyperopt show
# main.main(hyperopt_show(e= 233))

#! strayegy update
# main.main(strategy_update())

#! backtesting show
# main.main(backtesting_show())

#! hyperopt list
# main.main(hyperopt_list())

#! install ui
# main.main(install_ui())

#! look ahead
# main.main(look_ahead(s='mom' , d= 30))

#! resourceive analyze
# main.main(resourcive_analyze(s= 'mom' , d= 30))

#! list strategies
# main.main(list_strategies())

#! plotting
# main.main(plot_dataframe(s='hoo' , p= "POPCAT/USDT:USDT"))

#! new strategy
# main.main(new_strategy(s="mom" , t='advanced'))



#! test pairlist
# main.main(test_pairlist())

#! download  data
# main.main(download_data(e='bybit' , d=60 , tf='1m'))

# main.main(download_data(e='bybit' , d=35 , tf='1h'))

# main.main(download_data(d=30 , tf='5m'))



# # ! hyper opt
# del_hyperopt_result()

# 'stoploss'
# 'roi'
# 'trailing'
# 'protection'

# main.main(hyperopt(s='st3', loss= 'ShortTradeDurHyperOptLoss' ,e= 250 , d= 30 , spaces=['buy' , 'sell' , 'roi' , 'stoploss', 'trailing'] ,use_detail_time= False))

main.main(hyperopt(s='MainStrategy5', loss='OnlyProfitHyperOptLoss' ,e= 400 ,d=30 , spaces=['buy' , 'sell' , 'stoploss', 'trailing'] , use_detail_time= False))

# main.main(hyperopt(s='jef', loss='MultiMetricHyperOptLoss'  ,e= 250 ,d=30 , spaces=['buy' , 'sell' , 'roi' , 'stoploss' , 'trailing'] , j= 12 ,use_detail_time= False))

# main.main(hyperopt(s='jef', loss='CalmarHyperOptLoss' ,e= 150 ,d=30 , spaces=['buy' , 'sell' , 'roi' , 'stoploss' , 'trailing'] , j= 12 ,use_detail_time= False))

# main.main(hyperopt(s='kol', loss='MaxDrawDownRelativeHyperOptLoss' ,e= 500 ,d=30 , spaces=['buy' , 'sell' , 'roi' , 'stoploss' , 'trailing'] , j= 12 ,use_detail_time= False))

# main.main(hyperopt(s='kol', loss='SortinoHyperOptLoss' ,e= 400 ,d=30 , spaces=['buy' , 'sell' , 'roi' , 'stoploss' , 'trailing'] , j= 12 ,use_detail_time= False))

# main.main(hyperopt(s='javad', loss='ProfitDrawDownHyperOptLoss' ,e= 150 ,d=30 , spaces=['stoploss' , 'trailing'] , use_detail_time= False))


# =============! backtest
# main.main(backtest(s= 'Strategy005', d= 20))

#!======== delete folders content
# del_downloaded_data()
# del_backtest_results()



# python -m  compileall bot21.py
# python -m cProfile -s cumulative your_script.py