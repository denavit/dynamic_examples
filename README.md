MEETING QUESTIONS/TOPICS

- Is it truly more efficient to have all the html pages separate? There is very little that would be left by the time a chunk of the text is moved into Python
- Should the calculations for dmin, d2min, D1bsc, etc. be included unde geometric properties? Or should those be in a different section like "derivation of properties"

IMPORTANT NOTES

- Pages should initially be built under "templates," with text in the python side. The input/header text can then be moved over once the page is functionally and textually finalized

IMMEDIATE ACTION ITEMS

- create "base" html file
- modify ScrewThreadLib to just be functions that can be used, but each value must be calculated individually prior to text generation instead of within text generation
- Bolt page text
- bolt page functionality
- Add calculate button next to dropdown for wide flange page
- move html to python page text file

LONG TERM ACTION ITEMS

- add hyperlinks to standards
- implement nav bar on each page

AESTHETIC ACTION ITEMS

- make nav bar dropdown, hidden then appear when hovering, etc.
- make .button look better
- rearrange inputs and select on bolt page
- wide flange inputs out of alignment. why?

NOTES

- Bolt selection is working. Just needs page text.

  - I'd suggest making a comprehensive list of bolts and add them. If a student discovers one they need then it can be added to the dropdown. I don't see much purpose in allowing custom inputs, partially because I couldn't wrap my head around the logic of how to go about that (granted I may just need more time with it)

- Can add "onchange='this.form.submit()'" to make page reload upon user input, however it is not smooth and refreshes the page each time. Whether there is a way to seamlessly update the page I do not know

  - AJAX looks to be a possibility for this, need to learn more
    - might not be possible because of the use of flask and python but im not sure

- Can add "onchange='this.form.submit()'" to make page reload upon user input, however it is not smooth and refreshes the page each time. Whether there is a way to seamlessly update the page I do not know

Create class to build HTML output.

html_str = html_str_generator(indent=6)
html_str.append('heading','h1')
html_str.append('text','p')
html_str.append(r'$P_n = F_y A_g$','p')
html_str.append_part('partial line of text')
