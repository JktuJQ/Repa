# Database of educational materials with the ability to download notes, cheat sheets and manuals for various disciplines

![Репа](docs/image.png)

## Application goal

A common problem in universities is searching for educational materials.
Searching for disparate sources takes a lot of time and it is often difficult to navigate in a dump of hundreds of documents.

**Repa** is designed to solve this problem by adding additional functionality for the convenience of users.

## Project objectives
To solve the problem described above, we decided to create a system that allows
1. storing notes and lecture recordings in an organized manner,
2. sharing high-quality photos of notes due to automatic processing,
3. watching lectures, or rather the most important moments from them, in the format of such addictive vertical videos.

## Website interface

Login page:

![Login page](docs/login_page.png)

Main menu:

![Main menu](docs/main_page.png)

Category page:

![Category page](docs/category_page.png)

File page:

![File page](docs/file_page.png)

File download page:

![File download page](docs/download_page.png)

## Note

This project was developed as part of a hackathon in a short time frame and,
as a result, the written code is subject to technical debt and clogging (this is especially true for the CSS file).

The functionality of special processing functions (cutting out a contour from a photo, converting video to vertical format)
is not presented through the site, but is available manually through scripts in the [ml](ml) folder.

However, the presented project is viable even in this state, and therefore may be an object of interest.
