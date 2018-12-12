# What you need to do?
* [ ] add correct information and assets about your company challenge and your team (see instructions below)
* [ ] for each team member, update your personal information in our [Cornell Studio Tech Directory](https://directory.cornelltech.io) (picture, bio, etc.). Note that you can choose to opt-out once you are in the Cornell Tech Directory.

For questions you may have, feel free to email [hellostudio@cornell.edu](mailto:hellostudio@cornell.edu?subject=Buildboard).

# Why?
For Product Challenge 2018, we are asking you to use Github to keep track of your progress.

For this purpose, we have created one private Github repo for each team, under ct-product-challenge-2018.

The name of the repository corresponds to the name and number of your company challenge.

# What is the private repo for?

Feel free to use the repository as you see fit.

The repo is private: only your team and the Studio team have access to the content of the repository.
Nbody else from Cornell Tech, nobody else from the outside.

# How do I provide data about my project?
For reporting, we ask you to create and update a special file called `report.yaml` inside this repository.
We will use this file to automatically generate reports and a website for all projects .

The report.yaml file used the YAML file format (syntax definition, on-line syntax checker) and should following the structure defined below.

We also ask you to upload logos, individual pictures and team pictures and provide a link in the `report.yaml` file.

Here is a concrete example from last year.

```yaml
company:
  name: Team Awesome
  logo: Cornell_NYC_Tech_logo.png
product_hmw: How might we showcase Cornell Tech students work?
product_narrative: |
  Cornell Tech students build some amazing things. But it is often hard to show it to outside people.
  With BuildBoard, we let students provide regular updates about their work and create a Web version of it.
team:
  picture: E383E868-.jpg
  roster:
  - name: Rachel Sobel
    email: rachel.sobel.cornell@gmail.com
    picture: rachel.jpg
    program: LLM
  - name: Arnaud Sahuguet
    email: arnaud.sahuguet@cornell.edu
    picture: arnaud.png
    program: MBA
assets:
- title: Sprint 1
  url: http://cornelltech.io/spice-up-your-personal-privacy-with-pepr/
- title: Sprint 2
  url: http://cornelltech.io/health-apps-on-steroids/
```

# How will this information be used?
This information will be used to generate a website featuring all product challenges.
* For last year Startup Studio: http://buildboard-10044.cornelltech.io/
* For this year Product Studio: http://buildboard-10044.cornelltech.io/fall-2018/

# How do I know if I did the right thing?
The output of our automated process writes to file `buildboard.log` in your team repository.
We try to provide feedback when things went wrong, e.g. missing file, bad YAML syntax, etc.
