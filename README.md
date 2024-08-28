IDEAS

- Add hyperlinks to noted standards
- Option for user to save a member in a dropdown that will automatically populate fields with saved values
  - Very unsure of how to go about this, probably involves local memory, cookies, etc.
- Modify ScrewThreadLib to accept custom inputs and create object for calculations **or** modify ScrewThreadLib to just be functions that can be used, but each value must be calculated individually prior to text generation instead of within text generation

TO-DO

- Make inputs update on text field change **or** add calculate button
  - maybe?
- add full nav bar at top with home button and other calculators????
  - Partially implemented. Need to make look better
- edit .button in css to be more visually appealing
- finish text for bolt page
- delete col-3, change col-1 to 25%, replace col-3 with col-2 and col-4 with col-3
- wide flange inputs out of alignment

NOTES

- Bolt selection is working. Just needs page text.
  - I'd suggest making a comprehensive list of bolts and add them. If a student discovers one they need then it can be added to the dropdown. I don't see much purpose in allowing custom inputs, partially because I couldn't wrap my head around the logic of how to go about that (granted I may just need more time with it)

- Can add "onchange='this.form.submit()'" to make page reload upon user input, however it is not smooth and refreshes the page each time. Whether there is a way to seamlessly update the page I do not know
  - AJAX looks to be a possibility for this, need to learn more

Create class to build HTML output.

html_str = html_str_generator(indent=6)
html_str.append('heading','h1')
html_str.append('text','p')
html_str.append(r'$P_n = F_y A_g$','p')
html_str.append_part('partial line of text')
