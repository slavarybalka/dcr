import pandas as pd
import numpy as np
from StringIO import StringIO



df = pd.read_csv('dcr.csv', header=2)

partners = ['CSUSM','Colorado Mesa','ULL','Miami',\
			'Purdue','UFS','UINDY','UNC Wilmington',\
			'UNM','URI','USC','USI','UTA','ASU','Baylor',\
			'BLCU','BoiseState','CSU','EMICH','FIU',\
			'Lamar','LASALLE','LSU','LSUA','LSUS','MC',\
			'NSC','FITCHBURGSTATE','NSUOK','NWMISSOURI',\
			'SE','TAMUCC','UAH','UC','UNF','UTC','UTPB',\
			'UTRGV','UTTyler','UWF','UW - Superior']

verticals = ['Nursing', 'Education', 'Business']

partner = input('Enter the partner... ')
vertical = input('Enter the vertical... ')
#partner = 'LSUA'
#vertical = 'Business'


dfpv = df.set_index("Partner").loc[partner].set_index("Vertical").loc[vertical]

#print dfpv
# Get Monthly Goals CPL for Partner/Vertical
cpl_goal_search = dfpv[dfpv['Device'] == "Total"]['CPL Goal'][0]
cpl_goal_display = dfpv[dfpv['Device'] == "Total"]['CPL Goal'][1]
cpl_goal_total = dfpv[dfpv['Device'] == "Total"]['CPL Goal'][2]

mtd_cpl_search = dfpv[dfpv['Device'] == "Total"]['CPL.61'][0]
mtd_cpl_display = dfpv[dfpv['Device'] == "Total"]['CPL.61'][1]
mtd_cpl_total = dfpv[dfpv['Device'] == "Total"]['CPL.61'][2]



# Get budget info

budget_search = dfpv[dfpv['Device'] == "Total"]['Month Budget'][0]
budget_display = dfpv[dfpv['Device'] == "Total"]['Month Budget'][1]
budget_total = dfpv[dfpv['Device'] == "Total"]['Month Budget'][2]

spend_search_prev = dfpv[dfpv['Device'] == "Total"]['Spend.29'][0]
spend_display_prev = dfpv[dfpv['Device'] == "Total"]['Spend.29'][1]
spend_total_prev = dfpv[dfpv['Device'] == "Total"]['Spend.29'][2]

spend_search = dfpv[dfpv['Device'] == "Total"]['Spend.61'][0]
spend_display = dfpv[dfpv['Device'] == "Total"]['Spend.61'][1]
spend_total = dfpv[dfpv['Device'] == "Total"]['Spend.61'][2]
#print spend_total

spend_fc_search = dfpv[dfpv['Device'] == "Total"]['Spend.62'][0]
spend_fc_display = dfpv[dfpv['Device'] == "Total"]['Spend.62'][1]
spend_fc_total = dfpv[dfpv['Device'] == "Total"]['Spend.62'][2]
print 

# Get lead info

leads_search = dfpv[dfpv['Device'] == "Total"]['Lead Goal'][0]
leads_display = dfpv[dfpv['Device'] == "Total"]['Lead Goal'][1]
leads_total = dfpv[dfpv['Device'] == "Total"]['Lead Goal'][2]

mtd_leads_search = dfpv[dfpv['Device'] == "Total"]['Leads.61'][0]
mtd_leads_display = dfpv[dfpv['Device'] == "Total"]['Leads.61'][1]
mtd_leads_total = dfpv[dfpv['Device'] == "Total"]['Leads.61'][2]

leads_yoy_search = dfpv[dfpv['Device'] == "Total"]['Leads.18'][0]
leads_yoy_display = dfpv[dfpv['Device'] == "Total"]['Leads.18'][1]
leads_yoy_total = dfpv[dfpv['Device'] == "Total"]['Leads.18'][2]

leads_prev_search = dfpv[dfpv['Device'] == "Total"]['Leads.29'][0]
leads_prev_display = dfpv[dfpv['Device'] == "Total"]['Leads.29'][1]
leads_prev_total = dfpv[dfpv['Device'] == "Total"]['Leads.29'][2]

leads_fc_search = dfpv[dfpv['Device'] == "Total"]['Leads.62'][0]
leads_fc_display = dfpv[dfpv['Device'] == "Total"]['Leads.62'][1]
leads_fc_total = dfpv[dfpv['Device'] == "Total"]['Leads.62'][2]

# compare months to see if the account growing


# calculate incremental CPL

inc_spend_diff = int(spend_fc_total.replace(',','')) - int(spend_total_prev.replace(',',''))
inc_lead_diff = int(leads_fc_total) - int(leads_prev_total)
inc_cpl = float(inc_spend_diff) / float(inc_lead_diff)

#print spend_fc_total
#print spend_total_prev
#print inc_spend_diff
#print inc_lead_diff
#print inc_cpl
# output CPL stats
print "\n"*10
print partner + ' stats (' + vertical + '):\n' 

if int(cpl_goal_total) > int(mtd_cpl_total):
	print "%s looks good, month to date CPL $" % partner + mtd_cpl_total.lstrip() \
		+ "is lower than the budgeted CPL $%s" % cpl_goal_total.lstrip() 

if int(cpl_goal_total) < int(mtd_cpl_total):
	difference = int(mtd_cpl_total) - int(cpl_goal_total)
	percentage = float(difference)/float(cpl_goal_total) * 100
	print "Month-to-date CPL $" + mtd_cpl_total.lstrip() + \
	"for %s is higher than the budgeted CPL $" % partner + cpl_goal_total.lstrip()\
	 + 'by ' + str( "%.1f" % percentage).strip() + '%.'




# output budget stats
if int(spend_fc_total.replace(',','')) > int(budget_total.replace(',','')):
	budget_diff = int(spend_fc_total.replace(',','')) - int(budget_total.replace(',',''))
	print "We are pacing to overspend by $%d" % budget_diff


else:
	print "We are on track with the budget goal for this month."

# output lead stats

if int(leads_fc_total) < int(leads_total):
	lead_diff = int(leads_total) - int(leads_fc_total)
	lead_percentage = (float(lead_diff)/float(leads_total))*100
	print "We are pacing to receive " + str('%.1f'%lead_percentage) + "% fewer leads than planned (" + leads_fc_total.strip() + " forecasted vs " + leads_total + "budgeted)."

else:
	print "We are pacing to meet our lead goal for this month.(" + leads_fc_total.strip() + " forecasted vs " + leads_total + "budgeted)."



# output incremental CPL
print "Incremental CPL rate is", inc_cpl


# compare previous month to YOY

if int(leads_yoy_total) < int(leads_prev_total):
	print "We got more leads last month than in the same month last year. (", leads_yoy_total,"vs",leads_prev_total,")."
else:
	print "We got fewer leads last month than in the same month last year. (" + leads_yoy_total.lstrip() + "leads in the same month last year vs " + leads_prev_total.lstrip() + "leads last month)."


print '\n'*3