import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__)))
import migrateEreserves as me

m = me.Migration()

m.runMigration()
