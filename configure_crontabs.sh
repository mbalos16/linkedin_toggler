# ----------------- Close ----------------- 
# Every Friday at 23:00
echo '0 23 * * 5    cd /app && python main.py --close' >> /etc/crontabs/root

# ----------------- Open ----------------- 
# Every Monday at 7:00
echo '0 7 * * 1     cd /app && python main.py --open' >> /etc/crontabs/root

# Update crontab
crontab /etc/crontabs/root