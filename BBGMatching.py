
import pandas as pd
import numpy as np
import collections
import re
from matplotlib import pyplot as plt
import seaborn as sns
import time

class bbg:
    
    def __init__(self, student, mentor, matches, coefficients= {'interc':2.02397, 'ind_common':0,'word_count':0 ,'tech_common':-1.25752, 'topic_common':0, 'extro':0, 'intro': -1.25207 , 'stud_experience_o':-0.69260 , 'prof_experience_o': 0 , 'ind_common_extro':0, 'ind_common_intro':0,'tech_common_extro':0,'tech_common_intro':0, 'topic_common_extro':0,'topic_common_intro':0.90907, 'ind_common_stud':0,'tech_common_stud': 0.67054 ,'topic_common_stud': 0,'stud_exp_prof':0.30732 }): 
        self.data_student = student
        self.data_mentor = mentor
        matches = pd.merge(matches, mentor, how = 'inner', on = 'advisor_nyc_id')[['advisee_nyc_id', 'advisor_nyc_id', 'prof_company_clean', 'sessiontopic']]
        self.test = pd.DataFrame(matches.groupby('advisee_nyc_id')['sessiontopic'].unique()).reset_index()
        matches0 = pd.DataFrame(matches.groupby('advisee_nyc_id')['advisor_nyc_id'].unique()).reset_index()
        matches1 = pd.DataFrame(matches.groupby('advisee_nyc_id')['prof_company_clean'].unique()).reset_index()
        matches2 = pd.DataFrame(matches.groupby('advisee_nyc_id').size().reset_index())
        matches2.columns = ['advisee_nyc_id', 'count']
        matches1 = pd.merge(matches1, matches2, how = 'inner', on ='advisee_nyc_id')
        self.data_matches = pd.merge(matches0, matches1, how = 'inner', on = 'advisee_nyc_id')
        #self.data_matches.to_csv('mdata.csv')
        self.coef_o =coefficients.copy()
        self.coef =coefficients
        #self.test= matches
        #test = pd.merge(matches, mentor, how = 'inner', on = 'advisor_nyc_id')[['advisee_nyc_id', 'advisor_nyc_id', 'sessiontopic' ]]
        
        #self.match_session = pd.merge(matches, mentor, how = 'inner', on = 'advisor_nyc_id')[['advisee_nyc_id', 'advisor_nyc_id', 'sessiontopic' ]]
        
    def coefficients(self, extro=None, ind_common=None, word_count = None,ind_common_extro=None, 
                     ind_common_intro=None, ind_common_stud_exp = None, interc = None, 
                     intro=None, prof_experience_o=None, stud_experience_o=None, stud_exp_prof=None, 
                     tech_common=None, tech_common_extro=None,tech_common_intro = None, 
                     tech_common_stud_exp = None, topic_common = None, topic_common_extro= None,
                     topic_common_intro= None, topic_common_stud_exp = None):
        self.coef = self.coef_o
        #return self.test
        if extro != None: self.coef['extro'] = extro
        if ind_common != None: self.coef['ind_common'] = ind_common
        if word_count != None: self.coef['word_count'] = word_count
        if ind_common_extro != None: self.coef['ind_common_extro'] = ind_common_extro
        if ind_common_intro != None: self.coef['ind_common_intro'] = ind_common_extro
        if ind_common_stud_exp != None: self.coef['ind_common_stud'] = ind_common_stud_exp
        if interc != None: self.coef['interc'] = interc
        if intro != None: self.coef['intro'] = intrp
        if prof_experience_o != None: self.coef['prof_experience_o'] = prof_experience_o
        if stud_exp_prof != None: self.coef['stud_exp_prof'] = stud_experience_o
        if stud_exp_prof != None: self.coef['stud_exp_prof'] = stud_exp_prof
        if tech_common != None: self.coef['tech_common'] = tech_common
        if tech_common_extro != None: self.coef['tech_common_extro'] = tech_common_extro
        if tech_common_intro != None: self.coef['tech_common_intro'] = tech_common_intro
        if tech_common_stud_exp != None: self.coef['tech_common_stud'] = tech_common_stud_exp
        if topic_common != None: self.coef['topic_common'] = topic_common
        if topic_common_extro != None: self.coef['topic_common_extro'] = topic_common_extro
        if topic_common_intro != None: self.coef['topic_common_intro'] = topic_common_intro
        if topic_common_stud_exp != None: self.coef['topic_common_stud'] = topic_common_stud_exp
        return self.coef
    def matrix(self):
        student = self.data_student.copy()
        prof_data = self.data_mentor.copy()
        a = np.zeros((len(student),len(prof_data)))
        for i in range(len(student)):
            for j in range(len(prof_data)):
                match =pd.concat([student.iloc[i,:], prof_data.iloc[j,:]], axis=0)
                match.loc['ind_common'] = int(not set(match.loc['stud_ind']).isdisjoint([match.loc['prof_industry1']]))
                match.loc['tech_common'] = int(not set(match.loc['stud_tech']).isdisjoint([match.loc['prof_techtype1']]))
                match.loc['topic_common'] = int(not set(match.loc['stud_topic']).isdisjoint(match.loc['prof_topic']))
                match.loc['extro'] = 1 if match.loc['personality'] == 'Extrovert' else 0
                match.loc['intro'] = 1 if match.loc['personality'] == 'Introvert' else 0
                match.loc['ind_common_extro'] = match.loc['ind_common']*match.loc['extro']
                match.loc['ind_common_intro'] = match.loc['ind_common']*match.loc['intro']
                match.loc['ind_common_stud'] = match.loc['ind_common']*match.loc['stud_experience_o']
                match.loc['stud_exp_prof'] = match.loc['stud_experience_o']*match.loc['prof_experience_o']
                match.loc['tech_common_extro'] = match.loc['tech_common']*match.loc['extro']
                match.loc['tech_common_intro'] = match.loc['tech_common']*match.loc['intro']
                match.loc['tech_common_stud'] = match.loc['tech_common']*match.loc['stud_experience_o']
                match.loc['topic_common_extro'] = match.loc['topic_common']*match.loc['extro']
                match.loc['topic_common_intro'] = match.loc['topic_common']*match.loc['intro']
                match.loc['topic_common_stud'] = match.loc['topic_common']*match.loc['stud_experience_o']
                match.loc['interc']=1
                match.loc['word_count']= len(set(match['stud_str_combined1']).intersection(match['prof_str_combined1']))

                
                logodds = np.exp(sum([match[x]*self.coef[x] for x in self.coef.keys()]))
                success = logodds/ (logodds+1)
                
                a[i,j] = success
                
            print('row ' + str(i))
        print('done')
                
        data = pd.DataFrame(a)
        #lst = ['none']+prof_data['advisor_nyc_id'].tolist()
        data.columns=prof_data['advisor_nyc_id'].tolist()
        data['id']= student['advisee_nyc_id'].tolist()
        cols = data.columns.tolist()
        cols =cols[-1:] + cols[:-1]
        data = data[cols]
        #return data
        data.to_csv('matrix.csv')
        #return data
                
            
    def match(self, cutoff = .75, advisee = None, advisor = None):
        start = time.time()
        print('matching has begun')
        if advisee != None:
            rest_stud = self.data_student
            rest_prof = self.data_mentor
            used= [] + advisor
            advisee_id = [] + advisee
            advisor_id = [] + advisor
            rate = [] + [.75 for x in advisee]
            test = []+ ['' for x in advisee]
            advisee_location =[] +[list(rest_stud.loc[rest_stud['advisee_nyc_id']==x]['stud_location'].values) for x in advisee]
            advisor_location=[]+ [list(rest_prof.loc[rest_prof['advisor_nyc_id']==x]['prof_location'].values) for x in advisor]
            stud_topic = [] + [list(rest_stud.loc[rest_stud['advisee_nyc_id']==x]['stud_topic'].values) for x in advisee]
            prof_topic1= []+ [list(rest_prof.loc[rest_prof['advisor_nyc_id']==x]['prof_topic1'].values) for x in advisor]
            prof_topic2 =[]+ [list(rest_prof.loc[rest_prof['advisor_nyc_id']==x]['prof_topic2'].values) for x in advisor]
        else:
            
            used= [] 
            advisee_id = [] 
            advisor_id = [] 
            rate = [] 
            test = []
            advisee_location =[] 
            advisor_location=[]
            stud_topic = []
            prof_topic1= []
            prof_topic2 =[]
        wave= self.data_student['wave'].tolist()[0]
        #returning students
        stud_ret= pd.merge(self.data_student, self.data_matches.copy(), on ='advisee_nyc_id', how = 'inner')
        stud_ret = stud_ret.loc[stud_ret['count'] >0]
        stud_ret =stud_ret.sample(frac=1)
        
        prof_data = self.data_mentor.sample(frac=1)
#         keys = ['advisee_nyc_id']
#         i1 = self.data_student.set_index(keys).index
#         i2 = stud_ret.set_index(keys).index
        stud_ret1= stud_ret.loc[stud_ret['stud_waveUserStatus']=='waitlist']
        stud_ret2= stud_ret.loc[stud_ret['stud_waveUserStatus']!='waitlist']
        stud_ret2= stud_ret2.sample(frac=1).reset_index(drop=True)
        stud_ret = pd.concat([stud_ret1, stud_ret2])
        stud_ret= stud_ret[~stud_ret.advisee_nyc_id.isin(advisee_id)]
        #pd.concat([df1, df2])
        #users_prof_test.sample(frac=1).reset_index(drop=True)
        #prof_data = self.data_mentor.sample(frac=1)   
        prof_data1= prof_data[(prof_data['prof_waveUserStatus']=='waitlist') | (prof_data['prof_is_vip']=='Y') ]
        prof_data2= prof_data[~ prof_data.advisor_nyc_id.isin(prof_data1.advisor_nyc_id)]
        #stud_rem= self.data_student[~self.data_student.advisee_nyc_id.isin(advisee_id)]
        prof_data2 = prof_data2.sample(frac=1).reset_index(drop=True)
        prof_data = pd.concat([prof_data1, prof_data2])
        prof_data= prof_data[~prof_data.advisor_nyc_id.isin(used)]
        #return prof_data.shape
        #return prof_data
#         used= []
#         advisee_id = []
#         advisor_id = []
#         rate = []
#         test = []
#         advisee_location =[]
#         advisor_location=[]
#         stud_topic = []
#         prof_topic1= []
#         prof_topic2 =[]
        for i in range(len(stud_ret)):
            prob=0
            for j in range(len(prof_data)):
                if (prof_data.iloc[j,:]['prof_company_clean'] not in stud_ret.iloc[i,]['prof_company_clean']) and (prof_data.iloc[j,:]['prof_location']==stud_ret.iloc[i,:]['stud_location']) and (prof_data.iloc[j,:]['advisor_nyc_id'] not in used) and (prof_data.iloc[j,:]['advisor_nyc_id'] not in stud_ret.iloc[i,:]['advisor_nyc_id']):
                    match =pd.concat([stud_ret.iloc[i,:], prof_data.iloc[j,:]], axis=0)
                    match.loc['ind_common'] = int(not set(match.loc['stud_ind']).isdisjoint([match.loc['prof_industry1']]))
                    match.loc['tech_common'] = int(not set(match.loc['stud_tech']).isdisjoint([match.loc['prof_techtype1']]))
                    match.loc['topic_common'] = int(not set(match.loc['stud_topic']).isdisjoint(match.loc['prof_topic']))
                    match.loc['extro'] = 1 if match.loc['personality'] == 'Extrovert' else 0
                    match.loc['intro'] = 1 if match.loc['personality'] == 'Introvert' else 0
                    match.loc['ind_common_extro'] = match.loc['ind_common']*match.loc['extro']
                    match.loc['ind_common_intro'] = match.loc['ind_common']*match.loc['intro']
                    match.loc['ind_common_stud'] = match.loc['ind_common']*match.loc['stud_experience_o']
                    match.loc['stud_exp_prof'] = match.loc['stud_experience_o']*match.loc['prof_experience_o']
                    match.loc['tech_common_extro'] = match.loc['tech_common']*match.loc['extro']
                    match.loc['tech_common_intro'] = match.loc['tech_common']*match.loc['intro']
                    match.loc['tech_common_stud'] = match.loc['tech_common']*match.loc['stud_experience_o']
                    match.loc['topic_common_extro'] = match.loc['topic_common']*match.loc['extro']
                    match.loc['topic_common_intro'] = match.loc['topic_common']*match.loc['intro']
                    match.loc['topic_common_stud'] = match.loc['topic_common']*match.loc['stud_experience_o']
                    match.loc['word_count']= len(set(match['stud_str_combined1']).intersection(match['prof_str_combined1']))
                    match.loc['interc']=1

                    #matching
                    logodds = np.exp(sum([match[x]*self.coef[x] for x in self.coef.keys()]))
                    success = logodds/ (logodds+1)

                    if success > cutoff:
                        used.append(prof_data.iloc[j,:]['advisor_nyc_id'])
                        advisee_id.append(stud_ret.iloc[i,:]['advisee_nyc_id'])
                        advisor_id.append(prof_data.iloc[j,:]['advisor_nyc_id'])
                        rate.append(success)
                        test.append(i)
                        advisee_location.append(stud_ret.iloc[i,:]['stud_location'])
                        advisor_location.append(prof_data.iloc[j,:]['prof_location'])
                        stud_topic.append(stud_ret.iloc[i,:]['stud_topic'])
                        prof_topic1.append(prof_data.iloc[j,:]['prof_topic1'])
                        prof_topic2.append(prof_data.iloc[j,:]['prof_topic2'])
                        break
                    elif success > prob:
                        prob = success.copy()
                        id_= j

                    if j== len(prof_data)-1:   
                        used.append(prof_data.iloc[id_,:]['advisor_nyc_id'])
                        advisee_id.append(stud_ret.iloc[i,:]['advisee_nyc_id'])
                        advisor_id.append(prof_data.iloc[id_,:]['advisor_nyc_id'])
                        rate.append(prob)
                        test.append(i)
                        advisee_location.append(stud_ret.iloc[i,:]['stud_location'])
                        advisor_location.append(prof_data.iloc[id_,:]['prof_location'])
                        stud_topic.append(stud_ret.iloc[i,:]['stud_topic'])
                        prof_topic1.append(prof_data.iloc[id_,:]['prof_topic1'])
                        prof_topic2.append(prof_data.iloc[id_,:]['prof_topic2'])
                        break
                elif j== len(prof_data)-1 and prob >0:   
                    used.append(prof_data.iloc[id_,:]['advisor_nyc_id'])
                    advisee_id.append(stud_ret.iloc[i,:]['advisee_nyc_id'])
                    advisor_id.append(prof_data.iloc[id_,:]['advisor_nyc_id'])
                    rate.append(prob)
                    test.append(i)
                    advisee_location.append(stud_ret.iloc[i,:]['stud_location'])
                    advisor_location.append(prof_data.iloc[id_,:]['prof_location'])
                    stud_topic.append(stud_ret.iloc[i,:]['stud_topic'])
                    prof_topic1.append(prof_data.iloc[id_,:]['prof_topic1'])
                    prof_topic2.append(prof_data.iloc[id_,:]['prof_topic2'])
                    break
            #print('done: ' + str(len(advisee_id)))
        print('matching returning students')
        #return len(advisee_id) > len(set(advisee_id))
        stud_rem= self.data_student[~self.data_student.advisee_nyc_id.isin(advisee_id)]
        #return len(stud_rem)
        prof_data = prof_data[~prof_data.advisor_nyc_id.isin(used)]
        for i in range(len(stud_rem)):
            prob = 0
            for j in range(len(prof_data)):
                if (prof_data.iloc[j,:]['prof_location']==stud_rem.iloc[i,:]['stud_location']) and (prof_data.iloc[j,:]['advisor_nyc_id'] not in used):
                    match =pd.concat([stud_rem.iloc[i,:], prof_data.iloc[j,:]], axis=0)
                    match.loc['ind_common'] = int(not set(match.loc['stud_ind']).isdisjoint([match.loc['prof_industry1']]))
                    match.loc['tech_common'] = int(not set(match.loc['stud_tech']).isdisjoint([match.loc['prof_techtype1']]))
                    match.loc['topic_common'] = int(not set(match.loc['stud_topic']).isdisjoint(match.loc['prof_topic']))
                    match.loc['extro'] = 1 if match.loc['personality'] == 'Extrovert' else 0
                    match.loc['intro'] = 1 if match.loc['personality'] == 'Introvert' else 0
                    match.loc['ind_common_extro'] = match.loc['ind_common']*match.loc['extro']
                    match.loc['ind_common_intro'] = match.loc['ind_common']*match.loc['intro']
                    match.loc['ind_common_stud'] = match.loc['ind_common']*match.loc['stud_experience_o']
                    match.loc['stud_exp_prof'] = match.loc['stud_experience_o']*match.loc['prof_experience_o']
                    match.loc['tech_common_extro'] = match.loc['tech_common']*match.loc['extro']
                    match.loc['tech_common_intro'] = match.loc['tech_common']*match.loc['intro']
                    match.loc['tech_common_stud'] = match.loc['tech_common']*match.loc['stud_experience_o']
                    match.loc['topic_common_extro'] = match.loc['topic_common']*match.loc['extro']
                    match.loc['topic_common_intro'] = match.loc['topic_common']*match.loc['intro']
                    match.loc['topic_common_stud'] = match.loc['topic_common']*match.loc['stud_experience_o']
                    match.loc['word_count']= len(set(match['stud_str_combined1']).intersection(match['prof_str_combined1']))
                    match.loc['interc']=1

                    #matching
                    logodds = np.exp(sum([match[x]*self.coef[x] for x in self.coef.keys()]))
                    success = logodds/ (logodds+1)


                    if success > cutoff:
                        used.append(prof_data.iloc[j,:]['advisor_nyc_id'])
                        advisee_id.append(stud_rem.iloc[i,:]['advisee_nyc_id'])
                        advisor_id.append(prof_data.iloc[j,:]['advisor_nyc_id'])
                        rate.append(success)
                        test.append(i)
                        advisee_location.append(stud_rem.iloc[i,:]['stud_location'])
                        advisor_location.append(prof_data.iloc[j,:]['prof_location'])
                        stud_topic.append(stud_rem.iloc[i,:]['stud_topic'])
                        prof_topic1.append(prof_data.iloc[j,:]['prof_topic1'])
                        prof_topic2.append(prof_data.iloc[j,:]['prof_topic2'])
                        break
                    elif success > prob:
                        prob = success.copy()
                        id_= j

                    if j== len(prof_data)-1:
                        used.append(prof_data.iloc[id_,:]['advisor_nyc_id'])
                        advisee_id.append(stud_rem.iloc[i,:]['advisee_nyc_id'])
                        advisor_id.append(prof_data.iloc[id_,:]['advisor_nyc_id'])
                        prof_data.iloc[id_,:]['advisor_nyc_id']

                        rate.append(prob)
                        test.append(i) 
                        advisee_location.append(stud_rem.iloc[i,:]['stud_location'])
                        advisor_location.append(prof_data.iloc[id_,:]['prof_location'])
                        stud_topic.append(stud_rem.iloc[i,:]['stud_topic'])
                        prof_topic1.append(prof_data.iloc[id_,:]['prof_topic1'])
                        prof_topic2.append(prof_data.iloc[id_,:]['prof_topic2'])
                        break
                elif j== len(prof_data)-1 and prob >0:   
                    used.append(prof_data.iloc[id_,:]['advisor_nyc_id'])
                    advisee_id.append(stud_rem.iloc[i,:]['advisee_nyc_id'])
                    advisor_id.append(prof_data.iloc[id_,:]['advisor_nyc_id'])
                    rate.append(prob)
                    test.append(i)
                    advisee_location.append(stud_rem.iloc[i,:]['stud_location'])
                    advisor_location.append(prof_data.iloc[id_,:]['prof_location'])
                    stud_topic.append(stud_rem.iloc[i,:]['stud_topic'])
                    prof_topic1.append(prof_data.iloc[id_,:]['prof_topic1'])
                    prof_topic2.append(prof_data.iloc[id_,:]['prof_topic2'])
                    break
                            
                        
            #print('done: ' + str(len(advisee_id)))
        print('matching students based on location')
        
        ###################
        
        stud_region = self.data_student[~self.data_student['advisee_nyc_id'].isin(advisee_id)]
        stud_region = stud_region.loc[stud_region['stud_region']!='other']
        prof_data = prof_data[~prof_data['advisor_nyc_id'].isin(used)]
        for i in range(len(stud_region)):
            prob = 0
            for j in range(len(prof_data)):
                if (stud_region.iloc[i,:]['stud_location'] != 'other') and (prof_data.iloc[j,:]['prof_location']==stud_region.iloc[i,:]['stud_location']) and (prof_data.iloc[j,:]['advisor_nyc_id'] not in used):
                    match =pd.concat([stud_region.iloc[i,:], prof_data.iloc[j,:]], axis=0)
                    match.loc['ind_common'] = int(not set(match.loc['stud_ind']).isdisjoint([match.loc['prof_industry1']]))
                    match.loc['tech_common'] = int(not set(match.loc['stud_tech']).isdisjoint([match.loc['prof_techtype1']]))
                    match.loc['topic_common'] = int(not set(match.loc['stud_topic']).isdisjoint(match.loc['prof_topic']))
                    match.loc['extro'] = 1 if match.loc['personality'] == 'Extrovert' else 0
                    match.loc['intro'] = 1 if match.loc['personality'] == 'Introvert' else 0
                    match.loc['ind_common_extro'] = match.loc['ind_common']*match.loc['extro']
                    match.loc['ind_common_intro'] = match.loc['ind_common']*match.loc['intro']
                    match.loc['ind_common_stud'] = match.loc['ind_common']*match.loc['stud_experience_o']
                    match.loc['stud_exp_prof'] = match.loc['stud_experience_o']*match.loc['prof_experience_o']
                    match.loc['tech_common_extro'] = match.loc['tech_common']*match.loc['extro']
                    match.loc['tech_common_intro'] = match.loc['tech_common']*match.loc['intro']
                    match.loc['tech_common_stud'] = match.loc['tech_common']*match.loc['stud_experience_o']
                    match.loc['topic_common_extro'] = match.loc['topic_common']*match.loc['extro']
                    match.loc['topic_common_intro'] = match.loc['topic_common']*match.loc['intro']
                    match.loc['topic_common_stud'] = match.loc['topic_common']*match.loc['stud_experience_o']
                    match.loc['word_count']= len(set(match['stud_str_combined1']).intersection(match['prof_str_combined1']))
                    match.loc['interc']=1

                    #matching
                    logodds = np.exp(sum([match[x]*self.coef[x] for x in self.coef.keys()]))
                    success = logodds/ (logodds+1)

                    if success > cutoff:
                        used.append(prof_data.iloc[j,:]['advisor_nyc_id'])
                        advisee_id.append(stud_region.iloc[i,:]['advisee_nyc_id'])
                        advisor_id.append(prof_data.iloc[j,:]['advisor_nyc_id'])

                        rate.append(success)
                        test.append(i)
                        advisee_location.append(stud_region.iloc[i,:]['stud_location'])
                        advisor_location.append(prof_data.iloc[j,:]['prof_location'])
                        stud_topic.append(stud_region.iloc[i,:]['stud_topic'])
                        prof_topic1.append(prof_data.iloc[j,:]['prof_topic1'])
                        prof_topic2.append(prof_data.iloc[j,:]['prof_topic2'])
                        break
                    elif success > prob:
                        prob = success.copy()
                        id_= j
                    if j== len(prof_data)-1:
                        used.append(prof_data.iloc[id_,:]['advisor_nyc_id'])
                        advisee_id.append(stud_region.iloc[i,:]['advisee_nyc_id'])
                        advisor_id.append(prof_data.iloc[id_,:]['advisor_nyc_id'])
                        rate.append(prob)
                        test.append(i) 
                        advisee_location.append(stud_region.iloc[i,:]['stud_location'])
                        advisor_location.append(prof_data.iloc[id_,:]['prof_location'])
                        stud_topic.append(stud_region.iloc[i,:]['stud_topic'])
                        prof_topic1.append(prof_data.iloc[id_,:]['prof_topic1'])
                        prof_topic2.append(prof_data.iloc[id_,:]['prof_topic2'])
                        break
                elif j== len(prof_data)-1 and prob >0:   
                    used.append(prof_data.iloc[id_,:]['advisor_nyc_id'])
                    advisee_id.append(stud_region.iloc[i,:]['advisee_nyc_id'])
                    advisor_id.append(prof_data.iloc[id_,:]['advisor_nyc_id'])
                    rate.append(prob)
                    test.append(i)
                    advisee_location.append(stud_region.iloc[i,:]['stud_location'])
                    advisor_location.append(prof_data.iloc[id_,:]['prof_location'])
                    stud_topic.append(stud_region.iloc[i,:]['stud_topic'])
                    prof_topic1.append(prof_data.iloc[id_,:]['prof_topic1'])
                    prof_topic2.append(prof_data.iloc[id_,:]['prof_topic2'])
                    break
                            
                        
            #print('done: ' + str(len(advisee_id)))
        ###################
        
        print('matching students based on region')        
        stud_unmatched = self.data_student[~self.data_student.advisee_nyc_id.isin(advisee_id)]
        #return(len(stud_unmatched), len(advisee_id))
        #return (len(stud_unmatched) )
        prof_data = prof_data[~prof_data.advisor_nyc_id.isin(used)]
        #print(str(len(stud_unmatched)) + '-----' +str(len(prof_data)))
        prob = 0
        for i in range(len(stud_unmatched)):
            prob = 0
            for j in range(len(prof_data)):
                if (prof_data.iloc[j,:]['advisor_nyc_id'] not in used):
                    match =pd.concat([stud_unmatched.iloc[i,:], prof_data.iloc[j,:]], axis=0)
                    match.loc['ind_common'] = int(not set(match.loc['stud_ind']).isdisjoint([match.loc['prof_industry1']]))
                    match.loc['tech_common'] = int(not set(match.loc['stud_tech']).isdisjoint([match.loc['prof_techtype1']]))
                    match.loc['topic_common'] = int(not set(match.loc['stud_topic']).isdisjoint(match.loc['prof_topic']))
                    match.loc['extro'] = 1 if match.loc['personality'] == 'Extrovert' else 0
                    match.loc['intro'] = 1 if match.loc['personality'] == 'Introvert' else 0
                    match.loc['ind_common_extro'] = match.loc['ind_common']*match.loc['extro']
                    match.loc['ind_common_intro'] = match.loc['ind_common']*match.loc['intro']
                    match.loc['ind_common_stud'] = match.loc['ind_common']*match.loc['stud_experience_o']
                    match.loc['stud_exp_prof'] = match.loc['stud_experience_o']*match.loc['prof_experience_o']
                    match.loc['tech_common_extro'] = match.loc['tech_common']*match.loc['extro']
                    match.loc['tech_common_intro'] = match.loc['tech_common']*match.loc['intro']
                    match.loc['tech_common_stud'] = match.loc['tech_common']*match.loc['stud_experience_o']
                    match.loc['topic_common_extro'] = match.loc['topic_common']*match.loc['extro']
                    match.loc['topic_common_intro'] = match.loc['topic_common']*match.loc['intro']
                    match.loc['topic_common_stud'] = match.loc['topic_common']*match.loc['stud_experience_o']
                    match.loc['word_count']= len(set(match['stud_str_combined1']).intersection(match['prof_str_combined1']))
                    match.loc['interc']=1

                            #matching
                    logodds = np.exp(sum([match[x]*self.coef[x] for x in self.coef.keys()]))
                    success = logodds/ (logodds+1)

                    if success > cutoff:
                        used.append(prof_data.iloc[j,:]['advisor_nyc_id'])
                        advisee_id.append(stud_unmatched.iloc[i,:]['advisee_nyc_id'])
                        advisor_id.append(prof_data.iloc[j,:]['advisor_nyc_id'])
                        rate.append(success)
                        test.append(i)
                        advisee_location.append(stud_unmatched.iloc[i,:]['stud_location'])
                        advisor_location.append(prof_data.iloc[j,:]['prof_location'])
                        stud_topic.append(stud_unmatched.iloc[i,:]['stud_topic'])
                        prof_topic1.append(prof_data.iloc[j,:]['prof_topic1'])
                        prof_topic2.append(prof_data.iloc[j,:]['prof_topic2'])
                        break
                    elif success > prob:
                        prob = success.copy()
                        id_= j
                    if j == len(prof_data)-1:
                        used.append(prof_data.iloc[id_,:]['advisor_nyc_id'])
                        advisee_id.append(stud_unmatched.iloc[i,:]['advisee_nyc_id'])
                        advisor_id.append(prof_data.iloc[id_,:]['advisor_nyc_id'])
                        rate.append(prob)
                        test.append(i)
                        advisee_location.append(stud_unmatched.iloc[i,:]['stud_location'])
                        advisor_location.append(prof_data.iloc[id_,:]['prof_location'])
                        stud_topic.append(stud_unmatched.iloc[i,:]['stud_topic'])
                        prof_topic1.append(prof_data.iloc[id_,:]['prof_topic1'])
                        prof_topic2.append(prof_data.iloc[id_,:]['prof_topic2'])
        print('almost done')
                        
                            

        
        data_set= pd.DataFrame({'advisee_id': advisee_id, 'advisor_id': advisor_id, 'prob': rate, 'advisee location': advisee_location, 'advisor location': advisor_location, 'advisee topic' : stud_topic, 'advisor topic 1': prof_topic1, 'advisor topic 2': prof_topic2})
        matches_test = self.test.rename(index= str, columns={'advisee_nyc_id':'advisee_id', 'sessiontopic': 'advisee previous session topics'})
        matches_test = matches_test[['advisee_id', 'advisee previous session topics']]
        data_set= pd.merge(data_set, matches_test, on = 'advisee_id', how = 'left')
        #data_set['advisee previous session topics']= data_set['advisee previous session topics'].fillna('')
        data_set['session topic']= list(map(lambda a,b,c,d: a if (a not in [b] and a in c) else d if (d not in [b] and str(d) in c) else a,data_set['advisor topic 1'], data_set['advisee previous session topics'], data_set['advisee topic'], data_set['advisor topic 2']))
        data_set['wave']= wave
        data_set['location'] = list(map(lambda x,y: x if x==y else 'remote',data_set['advisee location'], data_set['advisor location'] ))
        data_set.to_csv('data.csv')
        print ('matching is done!')
        print('-'*100)
        print('the average match rate for all matches was :'+  str(np.mean(data_set['prob'])))
        print('-'*100)
        print('the top 5 matches were :')
        print(data_set['prob'].sort_values().tail())
        print('-'*100)
        print('the bottom 5 matches were :')
        print(data_set['prob'].sort_values().head())
        print('-'*100)
        sns.kdeplot(data_set['prob'], shade=True, label='Estimated Distribution')
        print('-'*100)
        end = time.time()
        print('time elapse: '+ str(end - start) + ' seconds')


        #return matches
                    