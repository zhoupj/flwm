from k.util.Logger import MyLogUtil;
from GlobalConfig import ConfigDict;

ml=MyLogUtil(ConfigDict['app_log_path'],ConfigDict['debug'],ConfigDict['console'])
logger=ml.logger;
digest_log=ml.digest_log;