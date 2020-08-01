/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev21.us', // the auth0 domain prefix
    audience: 'coffee_shop', // the audience set for the auth0 app
    clientId: 'Frh1OED5ev75o5vIO0gy69PJfF6sIWkZ', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:4200/tabs/user-page', // the base url of the running ionic application. 
  }
};
