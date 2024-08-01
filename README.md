IDEAS

- Add hyperlinks to noted standards
- Option for user to save a member in a dropdown that will automatically populate fields with saved values
  - Very unsure of how to go about this, probably involves local memory, cookies, etc.

TO-DO

- Make inputs update on text field change **or** add calculate button
- Make last selected member clear in local storage on page close
- add full nav bar at top with home button and other calculators????
  - Partially implemented. Need to make look better
- edit .button in css to be more visually appealing
- finish text for bolt page
- Fix pafe reset on bolt submit

NOTES

Create class to build HTML output.

html_str = html_str_generator(indent=6)
html_str.append('heading','h1')
html_str.append('text','p')
html_str.append(r'$P_n = F_y A_g$','p')
html_str.append_part('partial line of text')
