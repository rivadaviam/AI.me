# Troubleshooting Guide

## Common Issues

### AWS Connection Errors

**Problem**: Cannot connect to AWS services

**Solutions**:
- Verify AWS credentials
- Check AWS region configuration
- Verify IAM permissions

### Database Connection Errors

**Problem**: Cannot connect to database

**Solutions**:
- Verify database is running
- Check connection string
- Verify network access

### Import Errors

**Problem**: Module not found errors

**Solutions**:
- Activate virtual environment
- Install dependencies: `pip install -r requirements.txt`
- Check Python path

## Debugging

### Enable Debug Logging

```bash
export LOG_LEVEL=DEBUG
python -m src.api.main
```

### Check Logs

```bash
# Docker logs
docker logs ai-me

# Application logs
tail -f logs/app.log
```

## Getting Help

- Check documentation
- Review error messages
- Check GitHub issues
- Contact team

