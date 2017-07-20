# AP Daily Cost Analyzer created by Slava Rybalka (slava.rybalka@academicpartnerships.com)

import pandas as pd
import numpy as np

from Tkinter import *



df = pd.read_csv('dcr.csv', header=2)

#Getting the unique list of all partners from DCR
partners = df.Partner.unique()
#Getting the unique list of all verticals from DCR
verticals = df.Vertical.unique()


root = Tk()
root.title("AP DCR Analyzer")
mainframe = Frame(root)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 60, padx = 140)

partner_choices = map(np.unique, partners)
vertical_choices = map(np.unique, verticals)

################# dropdowns start

Label(mainframe, text="Choose a partner:").grid(row = 1, column = 1) 

var1 = StringVar(root)

partner_dropdown_menu = OptionMenu(mainframe,var1,*partners)
partner_dropdown_menu.config(width=20)
partner_dropdown_menu.grid(row = 2, column = 1)


Label(mainframe, text="Choose a vertical:").grid(row = 3, column = 1) 

var2 = StringVar(root)

vertical_dropdown_menu = OptionMenu(mainframe,var2,*verticals)
vertical_dropdown_menu.config(width=20)
vertical_dropdown_menu.grid(row = 4, column = 1)


#################### dropdown ends

def analyze():
    partner = var1.get()
    vertical = var2.get()


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

    leads_yoy_search = dfpv[dfpv['Device'] == "Total"]['Leads.17'][0]
    leads_yoy_display = dfpv[dfpv['Device'] == "Total"]['Leads.17'][1]
    leads_yoy_total = dfpv[dfpv['Device'] == "Total"]['Leads.17'][2]

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


    if int(cpl_goal_total) > int(mtd_cpl_total):
        #print "%s looks good, month to date CPL $" % partner + mtd_cpl_total.lstrip() \
        #   + "is lower than the budgeted CPL $%s" % cpl_goal_total.lstrip() 

        cpl_output = "%s looks good, month to date CPL $" % partner + mtd_cpl_total.lstrip() \
            + "is lower than the budgeted CPL $%s." % cpl_goal_total.strip()
        #print cpl_output 

    if int(cpl_goal_total) < int(mtd_cpl_total):
        difference = int(mtd_cpl_total) - int(cpl_goal_total)
        percentage = float(difference)/float(cpl_goal_total) * 100
        cpl_output = "Month-to-date CPL $" + mtd_cpl_total.lstrip() + \
        "for %s is higher than the budgeted CPL $" % partner + cpl_goal_total.lstrip()\
         + 'by ' + str( "%.1f" % percentage).strip() + '%.'
        #print cpl_output



    # output budget stats
    if int(spend_fc_total.replace(',','')) > int(budget_total.replace(',','')):
        budget_diff = int(spend_fc_total.replace(',','')) - int(budget_total.replace(',',''))
        budget_output = "\nWe are pacing to overspend by $%d." % budget_diff
        #print budget_output

    else:
        budget_output = "\nWe are on track with the budget goal for this month."
        #print budget_output

    # output lead stats

    if int(leads_fc_total) < int(leads_total):
        lead_diff = int(leads_total) - int(leads_fc_total)
        lead_percentage = (float(lead_diff)/float(leads_total))*100
        lead_stats_output = "\nWe are pacing to receive " + str('%.1f'%lead_percentage) + "% fewer leads than planned (" + leads_fc_total.strip() + " forecasted vs" + leads_total + "budgeted)."
        #print lead_stats_output


    else:
        lead_stats_output = "\nWe are pacing to meet our lead goal for this month.(" + leads_fc_total.strip() + " forecasted vs" + leads_total.lstrip() + "budgeted)."
        #print lead_stats_output


    # output incremental CPL
    incremental_cpl = "\nIncremental CPL rate is " + str('%.1f'%inc_cpl) + '.'
    #print incremental_cpl

    # compare previous month to YOY

    if int(leads_yoy_total) < int(leads_prev_total):
        leads_yoy_output = "\nWe got more leads last month than in the same month last year (" + leads_yoy_total.lstrip() + "vs " + leads_prev_total.strip() + ")."
        #print leads_yoy_output
    else:
        leads_yoy_output = "\nWe got fewer leads last month than in the same month last year (" + leads_yoy_total.lstrip() + "leads in the same month last year vs " + leads_prev_total.strip() + "leads last month)."
        #print leads_yoy_output


    # End insert

    result = cpl_output + '\n' + budget_output + '\n' + incremental_cpl + '\n'+ leads_yoy_output + '\n' + lead_stats_output
    


    text.delete(1.0, END)
    text.insert(END, result)

def center_window(width=300, height=200):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))





buttonAnalyze = Button(root, text='Analyze', width=10, command=analyze)
buttonAnalyze.grid(row = 5, column = 1, sticky='S')
buttonAnalyze.pack()

text = Text(root, height=20, width=60, wrap=WORD)
text.grid(column=1,row=5, columnspan=5, rowspan=1, sticky='N')
text.pack()


buttonQuit = Button(root, text='Quit', width=10, command=root.destroy)
buttonQuit.grid(row = 6, column = 1)
buttonQuit.pack()

#app = Application(master=root)
center_window(600, 600)
root.mainloop()
root.destroy()
