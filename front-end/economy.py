import requests
import pandas as pd
import re
import warnings
warnings.filterwarnings('ignore')
requests.packages.urllib3.disable_warnings()


def economy_clean(dataframe):
    transformed_economy_data = []
    for column in dataframe.columns:
        if column not in ['fin_yr', ' lga_name_2019', ' lga_code_2019'] and all(x not in column for x in ['bsnss_entrs','bsnss_entrs','indstry_emplynt', 'nmbr_bsnsss', 'registered_motor_vehicles', 'rgstrd_mtr_vhcls']):
            if 'business_entries' in column:
                type_ = 'business_entries'
            elif 'business_exits' in column:
                type_ = 'business_exits'
            elif 'number_of_businesses' in column and 'construction' in column:
                type_ = 'construction_businesses'
            elif 'number_of_businesses' in column and 'mining' in column:
                type_ = 'mining_businesses'
            elif 'number_of_businesses' in column and 'retail_trade' in column:
                type_ = 'retail_trade_businesses'
            elif 'ocptns_dbtrs_entrg' in column and 'clr_ad' in column:
                type_ = 'clerical_administrative_debtors'
            elif 'ocptns_dbtrs_entrg' in column and 'cmnty' in column:
                type_ = 'community_personal_service_debtors'
            elif 'ocptns_dbtrs_entrg' in column and 'lbrs_n' in column:
                type_ = 'labour_debtors'
            elif 'ocptns_dbtrs_entrg' in column and 'mchnry' in column:
                type_ = 'machinery_operators_and_drivers_debtors'
            elif 'ocptns_dbtrs_entrg' in column and 'mngrs' in column:
                type_ = 'manager_debtors'
            elif 'ocptns_dbtrs_entrg' in column and 'or_unk' in column:
                type_ = 'debtors_with_unknown_occupations'
            elif 'ocptns_dbtrs_entrg' in column and 'prfsnl' in column:
                type_ = 'professional_debtors'
            elif 'ocptns_dbtrs_entrg' in column and 'sl_wrk' in column:
                type_ = 'sales_debtors'
            elif 'ocptns_dbtrs_entrg' in column and 'tchns' in column:
                type_ = 'technicians_and_trades_debtors'
            elif 'prsnl_inslvncs' in column:
                type_ = 'personal_insolvencies'
            elif 'attchd_dwllngs_mdn_sle_prce' in column:
                type_ = 'median_price_attached_dwellings'
            elif 'hss_mdn_sle_prce' in column:
                type_ = 'median_sale_price_houses'
            elif 'hss_nmbr_trnsfrs_nm' in column:
                type_ = 'transfer_houses_num'
            elif 'atchd_dwlngs_nmbr_trnsf_nm' in column:
                type_ = 'transfer_attached_dwellings_num'
            elif 'bsn_rltd_csd_ecnm_cndts_nm' in column:
                type_ = 'personal_insolvencies_economic'
            elif 'bsn_rltd_csd_excsv_use_of' in column:
                type_ = 'personal_insolvencies_excessive_credit'
            elif 'bsn_rltd_csd_unmplyt_ls_o' in column:
                type_ = 'personal_insolvencies_loss_of_income'

            for index, value in dataframe[column].items():
                row_data = {
                    'year': dataframe[' yr'][index],
                    'lga_name': dataframe[' lga_name_2019'][index],
                    'lga_code': dataframe[' lga_code_2019'][index],
                    'type': type_,
                    'count': value
                }
                transformed_economy_data.append(row_data)
    return transformed_economy_data

def expand_and_merge_economy_data(dataframe):
    clean_data = economy_clean(dataframe)
    pivot_econmy_df = clean_data.pivot_table(index=['year', 'lga_name', 'lga_code'], columns='type', values='count', aggfunc = 'sum', fill_value=0)
    pivot_econmy_df.reset_index(inplace=True)
    pivot_econmy_df['debtor_num'] = pivot_econmy_df[[col for col in pivot_econmy_df.columns if 'debtors' in col]].sum(axis=1)
    pivot_econmy_df['businesses_num'] = pivot_econmy_df[[col for col in pivot_econmy_df.columns if 'businesses' in col]].sum(axis=1)
    pivot_econmy_df['personal_insolvencies_num'] = pivot_econmy_df[[col for col in pivot_econmy_df.columns if 'personal_insolvencies' in col]].sum(axis=1)
    cols_to_keep = [col for col in pivot_econmy_df.columns if not any(x in col for x in ['debtors', 'businesses', 'personal_insolvencies'])]
    cols_to_keep.extend(['businesses_num', 'personal_insolvencies_num'])
    economy_filtered = pivot_econmy_df[cols_to_keep]
    return economy_filtered


def clean_crime_data(dataframe):
    choose_col = [ ' reference_period', ' lga_code11', ' lga_name11', ' total_division_a_offences', ' total_division_b_offences', ' total_division_c_offences', ' total_division_d_offences', ' total_division_e_offences', ' total_division_f_offences']
    crime_total = dataframe[choose_col]
    crime_total.rename(columns={
        ' reference_period': 'year',
        ' lga_code11': 'lga_code',
        ' lga_name11': 'lga_name',
        ' total_division_a_offences': 'a_offences_num',
        ' total_division_b_offences': 'b_offences_num',
        ' total_division_c_offences': 'c_offences_num',
        ' total_division_d_offences': 'd_offences_num',
        ' total_division_e_offences': 'e_offences_num',
        ' total_division_f_offences': 'f_offences_num'
    }, inplace=True)
    return crime_total

def clean_population_data(dataframe):
    filtered_columns = dataframe.filter(regex='14|15|16|17|18|19').columns.tolist()
    pop_df = dataframe[filtered_columns]
    long_format = pd.DataFrame()

    key_columns = [' state_name_2021', ' lga_name_2021', ' lga_code_2021']
    use_col = [col.strip() for col in key_columns]
    pop_df.columns = pop_df.columns.str.strip()
    feature_columns = [col for col in pop_df.columns if col not in key_columns]

    for col in feature_columns:
        match = re.match(r'([a-zA-Z_]+)_(20\d{2})(?:_\d{2})?', col.strip())
        if match:
            type_name = match.group(1)
            year = match.group(2)
            temp_df = dataframe[key_columns].copy()  
            temp_df['variable'] = type_name
            temp_df['value'] = pop_df[col]
            temp_df['year'] = int(year)
            long_format = pd.concat([long_format, temp_df], ignore_index=True)

    long_format.columns = long_format.columns.str.strip()
    wide_format = long_format.pivot_table(index=use_col + ['year'], columns='variable', values='value').reset_index()
    wide_format = wide_format.rename(columns={
        'lga_code_2021': 'lga_code',
        'lga_name_2021': 'lga_name',
        'state_name_2021': 'state_name'
    }, inplace=True)
    return wide_format
    