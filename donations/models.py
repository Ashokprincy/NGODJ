class Campaign(models.Model):
    # ... your existing fields ...
    
    def get_progress_percent(self):
        if self.goal_amount <= 0:
            return 0
        progress = (self.raised_amount / self.goal_amount) * 100
        return min(progress, 100) # Prevents the bar from going past 100%
