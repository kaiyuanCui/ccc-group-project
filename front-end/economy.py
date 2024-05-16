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