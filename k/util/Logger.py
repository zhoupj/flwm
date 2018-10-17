
class Logger:

   debug=True;

   @staticmethod
   def log(*args):
       if(Logger.debug):
           print(args)

