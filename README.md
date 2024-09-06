MEETING QUESTIONS/TOPICS

- Should the calculations for dmin, d2min, D1bsc, etc. be included unde geometric properties? Or should those be in a different section like "derivation of properties"
- should the header, input, output, and footer be passed separately or added together and passed as one?
- should there be a navbar
- should the wide flange and bolt pages default to specific values?

IMPORTANT NOTES

- probably best to make pages in html first then transfer them over to python once the layout is done

IMMEDIATE ACTION ITEMS

- modify ScrewThreadLib to just be functions that can be used
- Bolt page text
- update tensile stress area equations to use \begin{aligned} and \end{aligned}

LONG TERM ACTION ITEMS

- add hyperlinks to standards
- implement nav bar on each page

AESTHETIC ACTION ITEMS

- make nav bar dropdown, hidden then appear when hovering, etc.
- make .button look better
- make text tab over on bolt page

NOTES

- Bolt selection is working. Just needs page text.

  - I'd suggest making a comprehensive list of bolts and add them. If a student discovers one they need then it can be added to the dropdown. I don't see much purpose in allowing custom inputs, partially because I couldn't wrap my head around the logic of how to go about that (granted I may just need more time with it)

- Can add "onchange='this.form.submit()'" to make page reload upon user input, however it is not smooth and refreshes the page each time. Whether there is a way to seamlessly update the page I do not know

Create class to build HTML output.

html_str = html_str_generator(indent=6)
html_str.append('heading','h1')
html_str.append('text','p')
html_str.append(r'$P_n = F_y A_g$','p')
html_str.append_part('partial line of text')
