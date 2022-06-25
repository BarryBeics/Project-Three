## Testing
<hr>

## Testing Index

- <a href="#code">1. Code validators</a>
- <a href="#responsive">2. Responsiveness</a>
- <a href="#browser">3. Browser compability</a>
- <a href="#test-user-stories">4. Testing user stories</a>
- <a href="#defensive">5. Defensive design</a>
- <a href="#bugs">6. Bugs</a>


<span id="code"></span>

## Code Validation
<hr>

The W3C Markup Validation Service was used to validate the HTML of the website.
### - - - - Public Pages

<details><summary>Landing Page</summary>
<img src="readme-docs/testing/html/landing_page.png">
</details>

<details><summary>Login Page</summary>
<img src="readme-docs/testing/html/login.png">
</details>

<details><summary>Register Page</summary>
<img src="readme-docs/testing/html/register.png">
</details>

### - - - - Logged In Pages

<details><summary>Chat Page</summary>
<img src="readme-docs/testing/html/chat.png">
</details>

<details><summary>Edit Activity Page</summary>
<img src="readme-docs/testing/html/edit_activity.png">
</details>

<details><summary>Edit Comment Page</summary>
<img src="readme-docs/testing/html/edit_comment.png">
</details>

<details><summary>Map Page</summary>
<img src="readme-docs/testing/html/map.png">
</details>

<details><summary>Post Activity Page</summary>
<img src="readme-docs/testing/html/post_activity.png">
</details>

<details><summary>Profile Page</summary>
<img src="readme-docs/testing/html/profile.png">
</details>

<details><summary>Register Group Page</summary>
<img src="readme-docs/testing/html/register_group.png">
</details>

<details><summary>Settings Page</summary>
<img src="readme-docs/testing/html/settings.png">
</details>

<details><summary>View Activity Page</summary>
<img src="readme-docs/testing/html/view_activity.png">
</details>

### - - - - Loading Pages

<details><summary>Landmark JSON Page</summary>
<img src="readme-docs/testing/html/landmark_json.png">
</details>

<details><summary>Map Link Page</summary>
<img src="readme-docs/testing/html/map_link.png">
</details>

<details><summary>Set Up JSON Page</summary>
<img src="readme-docs/testing/html/set_up.png">
</details>

<details><summary>User JSON Page</summary>
<img src="readme-docs/testing/html/user_json.png">
</details>

### - - - - Error Handling Pages

<details><summary>403, 404, 500 Page</summary>
<img src="readme-docs/testing/html/403_404_500.png">
</details>

### - - - - Admin Pages

<details><summary>Add Landmark Page</summary>
<img src="readme-docs/testing/html/add_landmark.png">
</details>

<details><summary>Admin Page</summary>
<img src="readme-docs/testing/html/admin.png">
</details>

<details><summary>Edit Group Page</summary>
<img src="readme-docs/testing/html/edit_group.png">
</details>

<details><summary>Edit Landmark Page</summary>
<img src="readme-docs/testing/html/edit_landmark.png">
</details>

<details><summary>Edit User Page</summary>
<img src="readme-docs/testing/html/edit_user.png">
</details>

<details><summary>Groups Page</summary>
<img src="readme-docs/testing/html/groups.png">
</details>

<details><summary>Landmarks Page</summary>
<img src="readme-docs/testing/html/landmarks.png">
</details>

<details><summary>Users Page</summary>
<img src="readme-docs/testing/html/users.png">
</details>

## CSS Validation
<hr>

The W3C Jigsaw CSS Validation Service was used to validate the CSS of the website. When validating all website, it passes with no errors.

<details><summary>style.css</summary>
<img src="readme-docs/testing/css/style.png">
</details>

## JavaScript Validation
<hr>

JSHint JS Validation Service was used to validate the Javascript files. No errors were found.

<details><summary>script.js</summary>
<img src="readme-docs/testing/js/script.png">
</details>

## PEP8 Validation
<hr>

PEP8 Validation Service was used to check the code for PEP8 requirements. All the code passes with no errors and no warnings to show.

<details><summary>init.py</summary>
<img src="readme-docs/testing/pep8/init.png">
</details>

<details><summary>models.py</summary>
<img src="readme-docs/testing/pep8/models.png">
</details>

<details><summary>routes.py</summary>
<img src="readme-docs/testing/pep8/routes.png">
</details>

<span id="responsive"></span>

## 2. Responsiveness
---
 
The responsive design tests were carried out manually whilst building the site with [Google Chrome DevTools](https://developer.chrome.com/docs/devtools/)
 
### 2.1. Mobiles ###

Notes:
- iPhone5, Galaxy S5/S6/S7 & Xperia Z3/Z3 :   Render fail, box breaks onto next line not as intended.

 
All the errors found have now been fixed as shown below.         
 
|        | iPhone 5 | iPhone 6/7 Plus | Galaxy S5/S6/S7 | Xperia Z3/Z3 | Google Pixel | Nexus 4 | Nexus 5/6 |
|--------|----------|-----------------|-----------------|--------------|--------------|---------|-----------|
| Render |  pass    |  pass           |  pass           |  pass        |  pass        |  pass   |  pass     |
| Images |  pass    |  pass           |  pass           |  pass        |  pass        |  pass   |  pass     |
| Links  |  pass    |  pass           |  pass           |  pass        |  pass        |  pass   |  pass     |
      
### 2.2. Tablets ###

Notes:
- iPad Pro :   Padding of half & third boxes needs increasing to display properly.
                                   
- Nexus 7:   Render fail, box breaks onto next line not as intended.
 
All the errors found have now been fixed as shown below.    
 
|        | iPad Mini | iPad Pro | Kindle Fire | Nexus 7 | Nexus 9 | Galaxy Tab 10 |
|--------|-----------|----------|-------------|---------|---------|---------------|
| Render |  pass     |  pass    |  pass       |  pass   |  pass   |  pass         |
| Images |  pass     |  pass    |  pass       |  pass   |  pass   |  pass         |
| Links  |  pass     |  pass    |  pass       |  pass   |  pass   |  pass         |
 
### 2.3. Desktops ###

Notes:
- All Sizes Desktop :   Padding of half & third boxes needs increasing to display properly.
 
All the errors found have now been fixed as shown below.
 
|        | 13" Desktop | 15" Desktop | 19" Desktop | 20" Desktop | 22" Desktop | 23" Desktop |
|--------|-------------|-------------|-------------|-------------|-------------|-------------|
| Render |  pass       |  pass       |  pass       |  pass       |  pass       |  pass       |
| Images |  pass       |  pass       |  pass       |  pass       |  pass       |  pass       |
| Links  |  pass       |  pass       |  pass       |  pass       |  pass       |  pass       |


<span id="browser"></span>

## Browser Compatibility

This site was tested on the following browsers with no visible issues for the user. Google Chrome, Safari and Mozilla Firefox. Appearance, functionality and responsiveness were consistent throughout for a range of device sizes and browsers.


<span id="test-user-stories"></span>

## Testing user stories



<span id="defensive"></span>

## Defensive design




<span id="bugs"></span>

## Bugs