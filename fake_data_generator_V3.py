import streamlit as st
import pandas as pd 
import numpy as np
import random
from datetime import date
from mimesis import Field
from mimesis.locales import Locale
from io import BytesIO



def erase(i):
	st.session_state[f'variable n°{i}']=""

def create_matrix(n):
	return [[] for k in range(n)]

def get_windows(nbre_variable):
	for i in range(nbre_variable):
		if f'variable n°{i}' not in st.session_state:
			st.session_state[f'variable n°{i}']=f'variable n°{i+1}'
	return st.tabs([st.session_state[f'variable n°{i}'] for i in range(nbre_variable)])

def get_Info(index_varaible,i):
	res=[]
	l,c,r=st.columns(3) 
	choice=l.selectbox('Which varaible do you want ?',('pre-made','personalized'),help='With the pre-made: you will use pre-made data base; with the personalized: you will need to provide it',key=f'{index_varaible}_{i}')
	res.append(choice)

	if choice=='pre-made':
		type_variable=c.selectbox('Wich data do you want ?',('Address','Finance','Datetime','Person','Science'),key=f'type_variable{i}{index_varaible}')
		lov_categories = ['Address','Finance','Datetime','Person','Science']
		address_lovs = ('address','calling_code','city','continent','coordinates','country','federal_subject','latitude','postal_code','province','region','street_name','street_number')
		finance_lovs = ('company','company_type','cryptocurrency_iso_code','currency_symbol')
		datetime_lovs = ('century','day_of_week','formatted_date','month')
		person_lovs = ('academic_degree','blood_type','email','full_name','gender','nationality','occupation','telephone','university')
		science_lovs = ('dn_asequence')
		lovs = [address_lovs, finance_lovs, datetime_lovs, person_lovs, science_lovs]
		dict_lovs = dict(zip(lov_categories, lovs))
		variable=r.selectbox(f'Which {type_variable} do you want ?', dict_lovs[type_variable], key=f'variable{i}_{index_varaible}')
		res.append(variable)

	else:
		type_variable=c.selectbox('wich type of data do you want ?',('int','float','categorical'),key=f'type{i}_{index_varaible}')
		res.append(type_variable)

		if type_variable=='float'or type_variable=='int':
			le,ri=st.columns(2)
			loi=r.selectbox('Wich law do you want ?',('uniform','gauss'),key=f'law{i}_{index_varaible}')
			res.append(loi)
			if loi=='uniform' :
				max_=le.number_input('value max',key=f'max{i}_{index_varaible}')
				min_=ri.number_input('value min',key=f'min{i}_{index_varaible}')
				res.append((min_,max_))
			elif loi=='gauss':
				moy=le.number_input('mean',key=f'moy{i}')
				sig=ri.number_input('standard error',key=f'sig{i}_{index_varaible}')
				res.append((moy,sig))
		else:
			nbre_category=r.number_input('How many category ?',min_value=1,max_value=12,step=1,key=f'nbre_category{i}_{index_varaible}')
			liste=[]
			list_weigth=[]
			columns=st.columns(6)
			for m in range(int(nbre_category//3)):
				for w in range(3):
					liste.append(columns[2*w].text_input('Category',key=f'quotient{i}{w}{m}_{index_varaible}'))
					list_weigth.append(columns[2*w+1].number_input('Weight',min_value=1,step=1,key=f'weight_quotient{i}{w}{m}_{index_varaible}'))
			for j in range(int(nbre_category%3)):
				liste.append(columns[2*j].text_input('Category',key=f'rest{i}{j}_{index_varaible}'))
				list_weigth.append(columns[2*j+1].number_input('Weight',min_value=1,step=1,key=f'weight_rest{i}{j}_{index_varaible}'))

			res.append(liste)
			res.append(list_weigth)
	return res

def get_behavior(variable_linked,i,index_varaible):
	l,r=st.columns(2)
	if variable_linked[2]=='categorical':
		return (st.multiselect('Wich categories do you want',variable_linked[3],key=f'list_behavior{i}{index_varaible}'))
			
	elif variable_linked[2]=='int':
		valeur_min=r.number_input('min value',step=1,key=f'valeur_min{i}{index_varaible}')
		valeur_max=l.number_input('max value',step=1,key=f'valeur_max{i}{index_varaible}')
		return ([valeur_min,valeur_max])

	elif variable_linked[2]=='float':
		valeur_min=r.number_input('min value',key=f'valeur_min{i}{index_varaible}')
		valeur_max=l.number_input('max value',key=f'valeur_max{i}{index_varaible}')
		return ([valeur_min,valeur_max])

def get_info_dependant(index_varaible,variable_linked,nbre_behavior):
	
	list_behavior=[]
	list_new_behavior=[]
	new_windows=st.tabs([f'behavior n°{k}' for k in range(int(nbre_behavior))])

	for i in range(int(nbre_behavior)):
		with new_windows[i]:
			list_behavior.append(get_behavior(variable_linked,index_varaible,i))
			list_new_behavior.append(get_Info(index_varaible,i))
	return(list_behavior,list_new_behavior)

def get_index_from_name(name,Name_variables):
	for i in range(len(Name_variables)):
		if name==Name_variables[i]:
			return i


def get_Names_Info(nbre_variable):
	
	
	windows=get_windows(nbre_variable)
	Name_variables=[]
	Info_variables=create_matrix(nbre_variable)
    
	for i in range(nbre_variable):
		with windows[i]:
			l,r=st.columns(2)
			l.text_input('Enter the name of the variable',key=f'variable n°{i}')
			Name_variables.append(st.session_state[f'variable n°{i}'])
			dependance=r.selectbox('Wich dependance do you want ?',('independant','dependant'),key=f'dependance{i}')
			Info_variables[i].append(dependance)

			if dependance=='independant':
				Info_variables[i]+=get_Info(i,50)
			else:
				list_independant=[Name_variables[k]  for k in range(len(Name_variables)) if (Info_variables[k][0]=='independant' and Info_variables[k][1]=='personalized')]
				name_dependance=l.selectbox('Dependance with wich variables ?',list_independant,key=f'index_dependance{i}')
				nbre_behavior=r.number_input('How many behavior do you want ?',step=1,min_value=1,key=f'behavior{i}')
				
				index_dependance=get_index_from_name(name_dependance,Name_variables)
				#pour les varaibles dependante 0: dependant 1: indexe de la variable de liason 2:liste des comportement(liste des categories ou doublet si int ou float 3:liste des nouvezaux comportements de la variable)
				Info_variables[i].append(index_dependance)
				l1,l2=get_info_dependant(i,Info_variables[index_dependance],nbre_behavior)
				Info_variables[i].append(l1)
				Info_variables[i].append(l2)
						
	return (Name_variables,Info_variables)

def get_one_value(variable_description):

	if variable_description[0]=='pre-made':
		field=Field(Locale.EN)
		_res=field(variable_description[1]) 
	else:
		if variable_description[1]=='float' or variable_description[1]=='int':
			if variable_description[2]=='uniform':
				mi,ma=variable_description[3]
				if variable_description[1]=='float':
					_res=random.uniform(mi,ma)
				else:
					_res=random.randint(int(mi),int(ma))

			elif variable_description[2]=='gauss':
				moy,sig=variable_description[3]
				if variable_description[2]=='float':
					_res=random.gauss(moy,sig)
				else:
					_res= int(random.gauss(int(moy),int(sig)))
		else:
			_res = random.choices(variable_description[2],weights=variable_description[3])[0]

	return _res

def get_values(Info_variables,nbre_ligne,nbre_variable):
	res=[]
	#a modifier info varaible arguments supplémentaire
	for i in range(nbre_variable):
		val=[]
		if Info_variables[i][0]=='independant':	
			for j in range(nbre_ligne):
				val.append(get_one_value(Info_variables[i][1:]))
		
		else:
			index_dependance=Info_variables[i][1]
			variable_linked=Info_variables[index_dependance]
			for j in range(nbre_ligne):
				k=0
				mod=False
				while k<len(Info_variables[i][2]) and mod == False:
					
					if variable_linked[2]=='categorical':
						if res[index_dependance][j] in Info_variables[i][2][k]:
							val.append(get_one_value(Info_variables[i][3][k]))
							mod = True
					else:
						min_,max_=Info_variables[i][2][k][0],Info_variables[i][2][k][1]
						if res[index_dependance][j] >= min_ and res[index_dependance][j]<max_:
							val.append(get_one_value(Info_variables[i][3][k]))
							mod=True
					k+=1
				if mod == False:
					val.append(None)
		res.append(val)
	return res


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')
@st.cache
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def main():
	st.title('Fake_Data_Generator')
	l,c,r=st.columns(3)
	
	name_file=l.text_input('Insert the name of the new file')
	nbre_ligne=int(c.number_input('How many rows do you want ?',step=1000))
	nbre_variable=int(r.number_input('How many variables do you want ?',min_value=1,step=1))

	Name_variables,Info_variables=get_Names_Info(nbre_variable)
	Values_Sample=get_values(Info_variables,5,nbre_variable)

	Sample = pd.DataFrame(dict(zip(Name_variables,Values_Sample)))
	st.header('Sample of the new data set')
	st.write(Sample.head())
	le,ce,ri=st.columns(3)

	if le.button('Create the new Data Set '):

		Values=get_values(Info_variables,nbre_ligne,nbre_variable)
		df_fake_data=pd.DataFrame(dict(zip(Name_variables,Values)))
		csv= convert_df(df_fake_data)
		df_excel = to_excel(df_fake_data)
				   
		ce.download_button(label="📥 Download (.csv)",data=csv,file_name=f'{name_file}.csv',mime='text/csv')
		ri.download_button(label="📥 Download (.xlsx)",data=df_excel,file_name=f'{name_file}.xlsx',mime='text/xlsx')
main()


