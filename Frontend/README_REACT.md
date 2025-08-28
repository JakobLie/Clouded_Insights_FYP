## Prerequisites

- Node.js (version 14 or higher)
[https://nodejs.org/en/download/]
- npm (comes with Node.js)


## Installing Dependencies
1. Navigate to correct directory `cd Frontend`
2. Run `npm install`

_In case of issues or missing dependencies, use `npm clean install`_ instead.

## Start Development Server
1. Run `npm run dev`

This launches the React app locally in development mode with features like hot module replacement and fast refresh.

2. Navigate to http://localhost:3000 to view the app.

Changes you make to the source code will be automatically reflected in the browser without needing to reload the page.

## Other Commands
- `npm install <package-name>`

Installs new packages and dependencies to the application.

-  `npm test`

Launches the test runner in the interactive watch mode.\
More info: https://facebook.github.io/create-react-app/docs/running-tests

- `npm run build`

Builds the app for production to the `build` folder.This bundles and optimises React in production mode for deployment.\
More info: https://facebook.github.io/create-react-app/docs/deployment

## Troubleshooting

- If you encounter issues with running `npx` due to execution policies (Windows), try running PowerShell as Administrator and set:  
  `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`
