#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 04:51:04 2020

@author: murali
"""
class pushtodb:
    def pushtodb(state_dic, users_dic):
        import pandas as pd
        import pymongo
        from pymongo import MongoClient
        client=MongoClient('mongodb+srv://---------------------------------')
        mydb=client['covid']
        information=mydb.collection
        information.delete_many({})
        information.insert_many(state_dic)
        #user info
        mydb=client['users']
        information=mydb.collection
        information.insert_many(users_dic)
        return None

