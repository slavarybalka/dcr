import pandas as pd
import numpy as np

from Tkinter import *








df = pd.read_csv('dcr.csv', header=2)

#Getting the unique list of all partners from DCR
partners = df.Partner.unique()
#Getting the unique list of all verticals from DCR
verticals = df.Vertical.unique()


#partner = input('Enter the partner... ')
#vertical = input('Enter the vertical... ')

partner = 'LSUA'
vertical = 'Business'

print 
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
	#print "%s looks good, month to date CPL $" % partner + mtd_cpl_total.lstrip() \
	#	+ "is lower than the budgeted CPL $%s" % cpl_goal_total.lstrip() 

	cpl_output = "%s looks good, month to date CPL $" % partner + mtd_cpl_total.lstrip() \
		+ "is lower than the budgeted CPL $%s" % cpl_goal_total.lstrip()
	print cpl_output 

if int(cpl_goal_total) < int(mtd_cpl_total):
	difference = int(mtd_cpl_total) - int(cpl_goal_total)
	percentage = float(difference)/float(cpl_goal_total) * 100
	cpl_output = "Month-to-date CPL $" + mtd_cpl_total.lstrip() + \
	"for %s is higher than the budgeted CPL $" % partner + cpl_goal_total.lstrip()\
	 + 'by ' + str( "%.1f" % percentage).strip() + '%.'
	print cpl_output



# output budget stats
if int(spend_fc_total.replace(',','')) > int(budget_total.replace(',','')):
	budget_diff = int(spend_fc_total.replace(',','')) - int(budget_total.replace(',',''))
	budget_output = "We are pacing to overspend by $%d" % budget_diff
	print budget_output

else:
	budget_output = "We are on track with the budget goal for this month."
	print budget_output

# output lead stats

if int(leads_fc_total) < int(leads_total):
	lead_diff = int(leads_total) - int(leads_fc_total)
	lead_percentage = (float(lead_diff)/float(leads_total))*100
	lead_stats_output = "We are pacing to receive " + str('%.1f'%lead_percentage) + "% fewer leads than planned (" + leads_fc_total.strip() + " forecasted vs " + leads_total + "budgeted)."
	print lead_stats_output


else:
	lead_stats_output = "We are pacing to meet our lead goal for this month.(" + leads_fc_total.strip() + " forecasted vs " + leads_total + "budgeted)."
	print lead_stats_output


# output incremental CPL
incremental_cpl = "Incremental CPL rate is" + str(inc_cpl)
print incremental_cpl

# compare previous month to YOY

if int(leads_yoy_total) < int(leads_prev_total):
	leads_yoy_output = "We got more leads last month than in the same month last year. (" + leads_yoy_total + "vs" + leads_prev_total + ")."
	print leads_yoy_output
else:
	leads_yoy_output = "We got fewer leads last month than in the same month last year. (" + leads_yoy_total.lstrip() + "leads in the same month last year vs " + leads_prev_total.lstrip() + "leads last month)."
	print leads_yoy_output

print '\n'*3




class Application(Frame):
    def say_hi(self):
        print "hi there, everyone!"

    def createWidgets(self):
        
      

        self.hi_there = Button(self)
        self.hi_there["text"] = "Analyze",
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left"})


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
root.title("AP DCR Analyzer")

mainframe = Frame(root)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 300, padx = 300)

tkvar = StringVar(root)
tkvar2 = StringVar(root)


partner_choices = map(np.unique, partners)
vertical_choices = map(np.unique, verticals)

tkvar.set('...') # set the default option
tkvar2.set('...') # set the default option
 
popupMenu = OptionMenu(mainframe, tkvar, *partner_choices)
Label(mainframe, text="Choose a partner").grid(row = 1, column = 1)
popupMenu.grid(row = 2, column = 1)
 
# on change dropdown value
def change_dropdown(*args):
    print( tkvar.get() )
 
# link function to change dropdown
tkvar.trace('w', change_dropdown)


popupMenu2 = OptionMenu(mainframe, tkvar2, *vertical_choices)
Label(mainframe, text="Choose a vertical").grid(row = 3, column = 1)
popupMenu2.grid(row = 4, column = 1)
 
# on change dropdown value
def change_dropdown2(*args):
    print( tkvar2.get() )
 
# link function to change dropdown
tkvar2.trace('w', change_dropdown2)


# textbox

S = Scrollbar(root)
T = Text(root, height=20, width=100)
S.pack(side=RIGHT, fill=Y)
T.pack(side=LEFT, fill=Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
quote = cpl_output + '\n' + budget_output + '\n' + incremental_cpl + '\n'+ leads_yoy_output + '\n' + lead_stats_output
T.insert(END, quote)


app = Application(master=root)
app.mainloop()
root.destroy()





