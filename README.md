IDEAS

- Add hyperlinks to noted standards
- Option for user to save a member in a dropdown that will automatically populate fields with saved values
  - Very unsure of how to go about this, probably involves local memory, cookies, etc.
- Modify ScrewThreadLib to accept custom inputs and create object for calculations **or** modify ScrewThreadLib to just be functions that can be used, but each value must be calculated individually prior to text generation instead of within text generation

TO-DO

- Make inputs update on text field change **or** add calculate button
- Make last selected member clear in local storage on page close
- add full nav bar at top with home button and other calculators????
  - Partially implemented. Need to make look better
- edit .button in css to be more visually appealing
- finish text for bolt page
- upon selecting a preset bolt, make inputs update with values of tabulated bolt data
- Differentiate tabulated bolts and custom bolts

NOTES

- Can add "onchange='this.form.submit()'" to make page reload upon user input, however it is not smooth and refreshes the page each time. Whether there is a way to seamlessly update the page I do not know

Create class to build HTML output.

html_str = html_str_generator(indent=6)
html_str.append('heading','h1')
html_str.append('text','p')
html_str.append(r'$P_n = F_y A_g$','p')
html_str.append_part('partial line of text')
