require('dotenv').config();

const port = process.env.PORT || 3000;
const databaseUri = process.env.MONGODB_URI;
const jwtSecret = process.env.JWT_SECRET;
const stripeApiKey = process.env.STRIPE_API_KEY;
const redisConfig = {  host: process.env.REDIS_HOST,
  port: process.env.REDIS_PORT,
  password: process.env.REDIS_PASSWORD,
};
const awsS3Config = {
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  region: process.env.AWS_REGION,
  bucketName: process.env.AWS_S3_BUCKET_NAME,};
const emailConfig = {
  service: process.env.EMAIL_SERVICE,
  user: process.env.EMAIL_USER,
  pass: process.env.EMAIL_PASS,
  from: process.env.EMAIL_FROM,
};

module.exports = {
  port,
  databaseUri,
  jwtSecret,
  stripeApiKey,  redisConfig,
  awsS3Config,
  emailConfig,
};
