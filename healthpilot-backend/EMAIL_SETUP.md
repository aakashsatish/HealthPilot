# Email Setup Guide

To enable email functionality for sending lab reports, you need to configure SMTP settings.

## Option 1: Gmail (Recommended for testing)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
3. **Add to your `.env` file**:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@healthpilot.com
```

## Option 2: Other Email Providers

### Outlook/Hotmail
```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your-email@outlook.com
SMTP_PASSWORD=your-password
FROM_EMAIL=noreply@healthpilot.com
```

### Yahoo
```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USERNAME=your-email@yahoo.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@healthpilot.com
```

## Option 3: No Email (Development)

If you don't want to set up email for development, the app will still work but emails won't be sent. You'll see a warning in the logs.

## Testing

1. Restart your backend server after adding the environment variables
2. Upload a lab report
3. Click the "📧 Email Report" button
4. Enter your email address
5. Check your inbox for the beautiful HTML report

## Email Features

- **Beautiful HTML Design** with HealthPilot branding
- **Complete Analysis** including summary, risk assessment, and recommendations
- **Lab Results Table** with color-coded status indicators
- **Professional Formatting** suitable for sharing with healthcare providers
- **Medical Disclaimer** included for legal compliance

## Troubleshooting

- **"Failed to send email"**: Check your SMTP credentials
- **"SMTP credentials not configured"**: Add the environment variables
- **Authentication errors**: Make sure you're using an app password, not your regular password
- **Port issues**: Try port 465 with SSL instead of 587 with TLS 