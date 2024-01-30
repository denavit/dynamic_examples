  IDEAS
  Add hyperlinks to noted standards
  Option for user to save a member in a dropdown that will automatically populate fields with saved values
    Very unsure of how to go about this, probably involves local memory, cookies, etc.

  TO-DO
  Make inputs update on text field change
    **Attempted to just check for a change and then submit the form but it did not submit. Unsure why it would not submit.**
    
  CURRENT ISSUES:
    **Can not get default member to show on the webpage. Why I believe this is happening:**
            1) Code runs through main.py, attempts to get member at line 12 of main.py, gets None (verified using print(member))
            2) Code generates "main_text" at line 127 of main.py, passing this through when "render_template" is called with the html page
            3) The page populates everything, with the script at line 64 of responsive_base.html setting the value of the select dropdown to the last value saved in local storage
            4) Because main.py runs first, it gets the value there at the time of it running, which is none. It only then populates with the value saved in local storage

      Potential Fixes?
        1) Somehow generate code then do member=request.form.get('member_dropdown')
        2) Pass value of selectItem from local storage BACK to flask after html page is loaded and populated
        3) Clear value of selectItem from local storage when page is closed, somehow default it back to a specific member that updates when selected
