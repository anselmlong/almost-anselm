🔍 Starting Exploratory Data Analysis for SFT Training Data
======================================================================
Loading data...
Successfully loaded 7560 conversations

============================================================
BASIC DATASET STATISTICS
============================================================
Total conversations: 7,560
Total messages: 97,848
Average messages per conversation: 12.94
Median messages per conversation: 5.00
Min messages per conversation: 1
Max messages per conversation: 209
Std deviation: 23.16

============================================================
ROLE DISTRIBUTION ANALYSIS
============================================================
Message count by role:
  assistant (me): 54,800 messages (56.0%)
  user: 43,048 messages (44.0%)

Average message length by role:
  assistant (me): 21.1 characters
  user: 22.2 characters

============================================================
CONTENT CHARACTERISTICS ANALYSIS
============================================================
Character count statistics:
  Mean: 21.6
  Median: 14.0
  Min: 1
  Max: 4091
  95th percentile: 52.0

Word count statistics:
  Mean: 4.5
  Median: 3.0
  Min: 1
  Max: 706

Short messages (<10 chars): 36855 (37.7%)
Long messages (>500 chars): 181 (0.2%)

Sample short messages:
  1: 'nvm'
  2: 'no la'
  3: 'ok'
  4: 'Xavier'
  5: 'haiz'

============================================================
CONVERSATION FLOW PATTERNS
============================================================
Conversation starters:
  assistant: 4917 (65.0%)
  user: 2643 (35.0%)

Conversation enders:
  assistant: 7555 (99.9%)
  user: 5 (0.1%)

Role transitions:
  assistant -> assistant: 31496 (34.9%)
  user -> user: 24656 (27.3%)
  user -> assistant: 18387 (20.4%)
  assistant -> user: 15749 (17.4%)

============================================================
LANGUAGE PATTERNS ANALYSIS
============================================================
URLs found: 583
Email addresses: 0
Hashtags: 67
Mentions: 437
Laugh expressions: 8431

Most common words:
  the: 9373
  but: 4630
  can: 4185
  and: 3954
  for: 3726
  like: 3478
  you: 3126

============================================================
DATA QUALITY ASSESSMENT
============================================================
⚠️  Data quality issues found:
  - Found 3542 messages with <3 characters

============================================================
GENERATING VISUALIZATIONS
============================================================
Visualization saved as 'eda_visualization.png'

============================================================
TRAINING RECOMMENDATIONS
============================================================
📊 Dataset Summary:
  - 7,560 conversations
  - 97,848 total messages
  - Average message length: 21.6 characters
  - 95th percentile length: 52.0 characters

💡 Recommendations:
  - Estimated average tokens per message: ~5
  - Consider max sequence length: 63 tokens
  - Medium dataset: Consider batch size 8-16
  - Multi-turn conversations: Focus on context preservation
  - Consider gradient accumulation if memory is limited
  - Monitor for overfitting with this dataset size

✅ EDA Complete! Check the generated visualization and summary above.
