'''
Command to run analysis of all stops
'''
import os
from django.core.management.base import BaseCommand, CommandError
from django.utils.importlib import import_module # Might be interna


class Command(BaseCommand):

    def handle(self, *args, **options):
        checks = self.find_checks(os.path.dirname(all_checks.__file__))
        if (len(args) > 0 and args[0] in checks):
            cmd = import_module('haltes.batch.checks.%s' % args[0]).Check()
            result = cmd.run()
            self.stdout.write(result)
        else:
            raise CommandError("Check does not exist or no check specified")
        
    def find_checks(self, path):
        ''' Copied from the django management interface. 
        Just listing all py files in a folder
        '''
        try:
            return [f[:-3] for f in os.listdir(path)
                    if not f.startswith('_') and f.endswith('.py')]
        except OSError:
            return []
                    
                                       


#            load_info = imp.find_module(module)
#            if load_info is not None:
#                imp.load_module(module, load_info[0], load_info[1], load_info[2])


#        sys.path.append(pkgpath)
#        for module in [name for _, name, _ in pkgutil.iter_modules([pkgpath])]:
#            pack = __import__(module)
#            for name in dir(pack):
#                try:
#                    print os.path.dirname(pack.__file__)
#                    load_info = imp.find_module(name, os.path.dirname(pack.__file__))
#                    print load_info
#                except ImportError:
#                    pass           