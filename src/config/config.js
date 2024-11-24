let configFile = {};

if (process.env.NEXT_PUBLIC_NODE_ENV === 'local') {
  configFile.API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL_LOCAL || '';
} else {
  configFile.API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
}

export {
  configFile
}