#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 09:10:13 2016

@author: thibaud
"""
import sys
from tools import log
import user_interface.django_config
import django
from user_interface.external_run import DjangoThread


def main():
    django.setup()

    # Start logging system
    log.config_logger()

    serveur_django = DjangoThread()
    serveur_django.start()

    try:
        serveur_django.join()
    except KeyboardInterrupt:
        print('########################### Interrupted #############################')
        serveur_django.stop_server()
        serveur_django.join()
        sys.exit(0)

# If main program, start main
if __name__ == "__main__":
    main()

