from k.util.Logger import MyLogUtil;
from GlobalConfig import ConfigDict;

ml=MyLogUtil(ConfigDict['app_log_path'],ConfigDict['debug'],ConfigDict['console'],'app')
logger=ml.logger;
digest_log=ml.digest_log;
suggest_log=ml.suggest_log;