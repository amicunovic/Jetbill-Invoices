import PyPDF2

import csv

import os


cost_m = ["MRC",]
product_m = ["Product",]
account_no = ["End Customer",]
account_master = ["Account",]
date_master = ["Date",]
product_group = ["Group",]
invoice_number = ["Reference",]

def radi10(something):




	opened_pdf = PyPDF2.PdfFileReader(something, 'rb')

	page_num = opened_pdf.getNumPages()

	pg = 0

	p1 = opened_pdf.getPage(0) # nadji prvu stranu da bi izvukao ime wholesale accounta
	p_text_p1 = p1.extractText()
	p_lines_p1 = p_text_p1.splitlines()

	while pg <= page_num - 1: # prolazim kroz stranice

		p = opened_pdf.getPage(pg) # otvara stranu
		p_text = p.extractText() #izvlaci text kao str
		p_lines = p_text.splitlines() # pravi list of strings 


		if "Description" in p_lines: # ako ima description - tako nalazim stranice koje imaju summaryije
			print(p_lines[1][6:])
			all_index = [] # lista za cost indexe
			min_range = p_lines.index("Description")
			all_index2 = [p_lines[min_range + 4]] #lista za product indexe koja jos sadrzi prvi product
			if "Total service charges excluding GST" in p_lines:
				max_range = p_lines.index("Total service charges excluding GST")
			else:
				max_range = len(p_lines) - 1
			p_lines1 = p_lines[max_range + 1:] #ogranicavam range ako postoje dva summarija na istoj strani da gleda samo drugi range
			account_invoice = p_lines_p1.index("Account No:") + 1 # koristim da nadjem ime glavnog accounta na prvoj strani
			p_lines_date = p_lines[min_range:max_range] # range za datum, isti kao i za kost
			all_index_date = [] # index lista za datum


			for text in p_lines[min_range:max_range]: # postavljen je maximum
				if "$" in text: #trazim $ na datoj strani
					all_index.append(text) #pakujem na listu
					cost = all_index[:] #skracujem listu - ovaj se ne koristi

					all_index_date = p_lines_date.index(text) - 2 # obelezavanje indexa datuma na osnovu $ sign pozicije
					date_prep = p_lines_date[all_index_date] # pakovanje datuma u master
					date_master.append(date_prep)

			for cost_num in cost: # pakujem glavni cost 
				cost_m.append(cost_num)
				account_no.append(p_lines[3]) #ubacujem ime usera sa strane gde je summary
				account_master.append(p_lines_p1[account_invoice]) # ubacujem ime glavnog accounta u glavnu listu
				product_group.append(p_lines[min_range-1]) # pakuje product group
				invoice_number.append(p_lines[1][6:]) # pakujem broj fakture


			if "Total service charges excluding GST" not in p_lines:
				cost_m.append(p_lines[max_range])
				account_no.append(p_lines[3]) #ubacujem ime usera sa strane gde je summary
				account_master.append(p_lines_p1[account_invoice]) # ubacujem ime glavnog accounta u glavnu listu
				date_master.append(p_lines[max_range - 2])
				product_group.append(p_lines[min_range-1]) # pakuje product group
				invoice_number.append(p_lines[1][6:])


			if "Description" in p_lines1: # ovo koristim da uzmem vrednosti iz drugog summarija ako postoji

				all_index10 = [] # lista za cost indexe
				min_range10 = p_lines1.index("Description")
				all_index11 = [p_lines1[min_range10 + 4]] #lista za product indexe koja jos sadrzi prvi product
				max_range10 = p_lines1.index("Total service charges excluding GST")
				account_invoice1 = p_lines_p1.index("Account No:") + 1 # za nalazenje imena accounta 
				p_lines_date10 = p_lines1[min_range10:max_range10] # range za datum, isti kao i za kost
				all_index_date10 = [] # index lista za datum
		

				for text in p_lines1[min_range10:max_range10]: # postavljen je maximum
					if "$" in text: #trazim $ na datoj strani
						all_index10.append(text) #pakujem na listu
						cost1 = all_index10[:] #skracujem listu

						all_index_date10 = p_lines_date10.index(text) - 2 # obelezavanje indexa datuma na osnovu $ sign pozicije
						date_prep10 = p_lines_date10[all_index_date10] # pakovanje datuma u master
						date_master.append(date_prep10)


				for cost_num in cost1: # pakujem glavni cost 
					cost_m.append(cost_num)
					account_no.append(p_lines[3]) #ubacujem ime usera sa strane gde je drugi summary
					account_master.append(p_lines_p1[account_invoice1]) #ubacujem ime glavnog accounta u glavnu listu iz drugog summarija
					product_group.append(p_lines1[min_range10 - 1]) # pakuje product group
					invoice_number.append(p_lines[1][6:])

			if "Total service charges excluding GST" in p_lines:		
				p_lines2 = p_lines[min_range:max_range+1]
			elif "Total service charges excluding GST" not in p_lines:
				p_lines2 = p_lines[min_range:max_range]


			itd = [i for i, item in enumerate(p_lines2) if item in cost] # poredim vrednosti dva skupa i izvlacim indexe onih koji se podudaraju
			for num in itd: # uzimam indexe jedan po jedan
				add1 = num + 1 # dodajem im 1 jer je se product nalazi na +1 index od costa
				all_index2.append(p_lines2[add1])
				product = all_index2[:-1]


			for product_num in product:
				if "Total service charges excluding GST" in product_num: #izbacujem naziv u "" jer se nalazi u product varijabli
					continue
				else:
					product_m.append(product_num)


			if "Total service charges excluding GST" not in p_lines: # ovo koristim da ubacim zadnji product ako se summary ne zavrsava na jednoj strani
				product_m.append(p_lines[max_range - 4])


			if "Description" in p_lines1: 
				if len(p_lines1[min_range10:max_range10]) < 11:  # Ako summary ima samo jedan product line, ovo sluzi da bi spakovao samo taj
					product_m.append(p_lines1[min_range10 + 4])

				else:
					p_lines3 = p_lines1[min_range10:max_range10]
					itd1 = [i for i, item in enumerate(p_lines3) if item in cost1] # poredim vrednosti dva skupa i izvlacim indexe onih koji se podudaraju
					for num in itd1: # uzimam indexe jedan po jedan
						add1 = num + 1 # dodajem im 1 jer je se product nalazi na +1 index od costa
						try:
							all_index11.append(p_lines3[add1])
							product1 = all_index11[:]
						except:
							pass
					try:		
						for product_num in product1:
							if "Total service charges excluding GST" in product_num: #izbacujem naziv u "" jer se nalazi u product varijabli
								continue
							else:
								product_m.append(product_num)
					except:
						pass


			pg += 1 #sledeca strana
			print(pg)
			print(something)

		elif "Total service charges excluding GST" in p_lines and not "Description" in p_lines: # ovo koristim da nadjem drugu stranu summarija koji se ne zavrsava na jednoj													
			all_index = [] # lista za cost indexe
			all_index2 = [p_lines[12]] #lista za product indexe koja jos sadrzi prvi product
			max_range = p_lines.index("Total service charges excluding GST")
			p_lines_date = p_lines[12:max_range] # range za datum, isti kao i za kost
			all_index_date = [] # index lista za datum
			account_invoice = p_lines_p1.index("Account No:") + 1 # koristim da nadjem ime glavnog accounta na prvoj strani

			if "Total service charges excluding GST" in p_lines[15:]: # ovo stavljam da isfiltriram ako na drugoj strani nema linija ali ima Total service charges... 
				for text in p_lines[12:max_range]: # postavljen je maximum
					if "$" in text: #trazim $ na datoj strani
						all_index.append(text) #pakujem na listu
						cost = all_index[:] #skracujem listu - ovaj se ne koristi
						all_index_date = p_lines_date.index(text) - 2 # obelezavanje indexa datuma na osnovu $ sign pozicije
						date_prep = p_lines_date[all_index_date] # pakovanje datuma u master
						date_master.append(date_prep)


				for cost_num in cost: # pakujem glavni cost 
					cost_m.append(cost_num)
					account_no.append(p_lines[3]) #ubacujem ime usera sa strane gde je summary
					account_master.append(p_lines_p1[account_invoice]) # ubacujem ime glavnog accounta u glavnu listu
					last_group = product_group[-1]
					product_group.append(last_group)
					invoice_number.append(p_lines[1][6:]) # pakujem broj fakture
						

				p_lines2 = p_lines[12:max_range + 1]
				itd = [i for i, item in enumerate(p_lines2) if item in cost] # poredim vrednosti dva skupa i izvlacim indexe onih koji se podudaraju
				for num in itd: # uzimam indexe jedan po jedan
					add1 = num + 1 # dodajem im 1 jer je se product nalazi na +1 index od costa
					all_index2.append(p_lines2[add1])
					product = all_index2[:-1]

				for product_num in product:
					if "Total service charges excluding GST" in product_num: #izbacujem naziv u "" jer se nalazi u product varijabli
						continue
					else:
						product_m.append(product_num)

				if "Description" in p_lines1:
					pg += 0 #sledeca strana
				else:
					pg += 1
					print(pg)
					print(something)
			else:
				pg += 1
				print(pg)
				print(something)

		else:
			pg += 1
			print(pg)
			print(something)



'''
	rows = zip(account_master, account_no, product_m, date_master, cost_m, product_group, invoice_number) # What will be imported in excel as a column

	with open(f"{file_name}.csv", "w", newline = '') as f:
	    writer = csv.writer(f)
	    for row in rows:
	        writer.writerow(row)
'''