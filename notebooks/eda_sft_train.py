#!/usr/bin/env python3
"""
Exploratory Data Analysis (EDA) for SFT Training Data
Analyzes the structure, patterns, and characteristics of the training dataset
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from collections import Counter, defaultdict
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set up plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_data(file_path):
    """Load the JSON data from file"""
    print("Loading data...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Successfully loaded {len(data)} conversations")
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def basic_statistics(data):
    """Generate basic statistics about the dataset"""
    print("\n" + "="*60)
    print("BASIC DATASET STATISTICS")
    print("="*60)
    
    total_conversations = len(data)
    total_messages = sum(len(conv['messages']) for conv in data)
    
    # Message counts per conversation
    msg_counts = [len(conv['messages']) for conv in data]
    
    print(f"Total conversations: {total_conversations:,}")
    print(f"Total messages: {total_messages:,}")
    print(f"Average messages per conversation: {np.mean(msg_counts):.2f}")
    print(f"Median messages per conversation: {np.median(msg_counts):.2f}")
    print(f"Min messages per conversation: {min(msg_counts)}")
    print(f"Max messages per conversation: {max(msg_counts)}")
    print(f"Std deviation: {np.std(msg_counts):.2f}")
    
    return {
        'total_conversations': total_conversations,
        'total_messages': total_messages,
        'msg_counts': msg_counts
    }

def role_analysis(data):
    """Analyze the distribution of roles (user vs assistant)"""
    print("\n" + "="*60)
    print("ROLE DISTRIBUTION ANALYSIS")
    print("="*60)
    
    role_counts = Counter()
    message_lengths_by_role = defaultdict(list)
    
    for conv in data:
        for msg in conv['messages']:
            role = msg['role']
            content = msg['content']
            role_counts[role] += 1
            message_lengths_by_role[role].append(len(content))
    
    print("Message count by role:")
    for role, count in role_counts.items():
        percentage = (count / sum(role_counts.values())) * 100
        print(f"  {role}: {count:,} messages ({percentage:.1f}%)")
    
    print("\nAverage message length by role:")
    for role, lengths in message_lengths_by_role.items():
        avg_length = np.mean(lengths)
        print(f"  {role}: {avg_length:.1f} characters")
    
    return role_counts, message_lengths_by_role

def content_analysis(data):
    """Analyze message content characteristics"""
    print("\n" + "="*60)
    print("CONTENT CHARACTERISTICS ANALYSIS")
    print("="*60)
    
    all_messages = []
    for conv in data:
        for msg in conv['messages']:
            all_messages.append(msg['content'])
    
    # Character counts
    char_counts = [len(msg) for msg in all_messages]
    
    # Word counts (rough estimate)
    word_counts = [len(msg.split()) for msg in all_messages]
    
    # Line counts
    line_counts = [len(msg.split('\n')) for msg in all_messages]
    
    print(f"Character count statistics:")
    print(f"  Mean: {np.mean(char_counts):.1f}")
    print(f"  Median: {np.median(char_counts):.1f}")
    print(f"  Min: {min(char_counts)}")
    print(f"  Max: {max(char_counts)}")
    print(f"  95th percentile: {np.percentile(char_counts, 95):.1f}")
    
    print(f"\nWord count statistics:")
    print(f"  Mean: {np.mean(word_counts):.1f}")
    print(f"  Median: {np.median(word_counts):.1f}")
    print(f"  Min: {min(word_counts)}")
    print(f"  Max: {max(word_counts)}")
    
    # Find very short and very long messages
    short_messages = [msg for msg in all_messages if len(msg) < 10]
    long_messages = [msg for msg in all_messages if len(msg) > 500]
    
    print(f"\nShort messages (<10 chars): {len(short_messages)} ({100*len(short_messages)/len(all_messages):.1f}%)")
    print(f"Long messages (>500 chars): {len(long_messages)} ({100*len(long_messages)/len(all_messages):.1f}%)")
    
    # Common patterns
    print(f"\nSample short messages:")
    for i, msg in enumerate(short_messages[:5]):
        print(f"  {i+1}: '{msg}'")
    
    return {
        'char_counts': char_counts,
        'word_counts': word_counts,
        'line_counts': line_counts,
        'short_messages': short_messages,
        'long_messages': long_messages
    }

def conversation_patterns(data):
    """Analyze conversation flow patterns"""
    print("\n" + "="*60)
    print("CONVERSATION FLOW PATTERNS")
    print("="*60)
    
    # Role transitions
    transitions = Counter()
    conversation_starters = Counter()
    conversation_enders = Counter()
    
    for conv in data:
        messages = conv['messages']
        if len(messages) > 0:
            # First and last message roles
            conversation_starters[messages[0]['role']] += 1
            conversation_enders[messages[-1]['role']] += 1
            
            # Role transitions
            for i in range(len(messages) - 1):
                current_role = messages[i]['role']
                next_role = messages[i + 1]['role']
                transitions[f"{current_role} -> {next_role}"] += 1
    
    print("Conversation starters:")
    for role, count in conversation_starters.items():
        percentage = (count / sum(conversation_starters.values())) * 100
        print(f"  {role}: {count} ({percentage:.1f}%)")
    
    print("\nConversation enders:")
    for role, count in conversation_enders.items():
        percentage = (count / sum(conversation_enders.values())) * 100
        print(f"  {role}: {count} ({percentage:.1f}%)")
    
    print("\nRole transitions:")
    for transition, count in transitions.most_common():
        percentage = (count / sum(transitions.values())) * 100
        print(f"  {transition}: {count} ({percentage:.1f}%)")
    
    return transitions, conversation_starters, conversation_enders

def language_analysis(data):
    """Analyze language patterns and characteristics"""
    print("\n" + "="*60)
    print("LANGUAGE PATTERNS ANALYSIS")
    print("="*60)
    
    all_content = []
    for conv in data:
        for msg in conv['messages']:
            all_content.append(msg['content'])
    
    # Join all content for analysis
    full_text = ' '.join(all_content)
    
    # Common patterns
    urls = re.findall(r'https?://[^\s]+', full_text)
    emails = re.findall(r'\S+@\S+', full_text)
    hashtags = re.findall(r'#\w+', full_text)
    mentions = re.findall(r'@\w+', full_text)
    
    # Emoji and emoticons (rough detection)
    laughs = len(re.findall(r'(haha|lol|lmao|😂|😄|😆)', full_text, re.IGNORECASE))
    
    print(f"URLs found: {len(urls)}")
    print(f"Email addresses: {len(emails)}")
    print(f"Hashtags: {len(hashtags)}")
    print(f"Mentions: {len(mentions)}")
    print(f"Laugh expressions: {laughs}")
    
    # Most common words (simple analysis)
    words = re.findall(r'\w+', full_text.lower())
    word_freq = Counter(words)
    
    print(f"\nMost common words:")
    for word, count in word_freq.most_common(15):
        if len(word) > 2:  # Skip very short words
            print(f"  {word}: {count}")
    
    return {
        'urls': urls,
        'emails': emails,
        'hashtags': hashtags,
        'mentions': mentions,
        'word_freq': word_freq
    }

def create_visualizations(stats, role_data, content_data):
    """Create visualizations of the data analysis"""
    print("\n" + "="*60)
    print("GENERATING VISUALIZATIONS")
    print("="*60)
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('SFT Training Data - Exploratory Data Analysis', fontsize=16, fontweight='bold')
    
    # 1. Messages per conversation distribution
    axes[0, 0].hist(stats['msg_counts'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('Distribution of Messages per Conversation')
    axes[0, 0].set_xlabel('Number of Messages')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].axvline(np.mean(stats['msg_counts']), color='red', linestyle='--', 
                       label=f'Mean: {np.mean(stats["msg_counts"]):.1f}')
    axes[0, 0].legend()
    
    # 2. Role distribution pie chart
    role_counts, message_lengths_by_role = role_data
    axes[0, 1].pie(role_counts.values(), labels=role_counts.keys(), autopct='%1.1f%%',
                   startangle=90, colors=['lightcoral', 'lightblue'])
    axes[0, 1].set_title('Distribution of Message Roles')
    
    # 3. Message length distribution
    axes[0, 2].hist(content_data['char_counts'], bins=50, alpha=0.7, 
                    color='lightgreen', edgecolor='black')
    axes[0, 2].set_title('Distribution of Message Lengths (Characters)')
    axes[0, 2].set_xlabel('Character Count')
    axes[0, 2].set_ylabel('Frequency')
    axes[0, 2].set_xlim(0, np.percentile(content_data['char_counts'], 95))
    
    # 4. Word count distribution
    axes[1, 0].hist(content_data['word_counts'], bins=50, alpha=0.7, 
                    color='orange', edgecolor='black')
    axes[1, 0].set_title('Distribution of Message Lengths (Words)')
    axes[1, 0].set_xlabel('Word Count')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].set_xlim(0, np.percentile(content_data['word_counts'], 95))
    
    # 5. Message length by role
    roles = list(message_lengths_by_role.keys())
    role_lengths = [message_lengths_by_role[role] for role in roles]
    axes[1, 1].boxplot(role_lengths, labels=roles)
    axes[1, 1].set_title('Message Length Distribution by Role')
    axes[1, 1].set_ylabel('Character Count')
    axes[1, 1].set_yscale('log')
    
    # 6. Conversation length categories
    msg_counts = stats['msg_counts']
    categories = ['1-2 msgs', '3-5 msgs', '6-10 msgs', '11-20 msgs', '20+ msgs']
    counts = [
        sum(1 for x in msg_counts if 1 <= x <= 2),
        sum(1 for x in msg_counts if 3 <= x <= 5),
        sum(1 for x in msg_counts if 6 <= x <= 10),
        sum(1 for x in msg_counts if 11 <= x <= 20),
        sum(1 for x in msg_counts if x > 20)
    ]
    
    axes[1, 2].bar(categories, counts, color='purple', alpha=0.7)
    axes[1, 2].set_title('Conversation Length Categories')
    axes[1, 2].set_ylabel('Number of Conversations')
    axes[1, 2].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('/home/anselmlong/Projects/almost-anselm/almost-anselm/notebooks/eda_visualization.png', 
                dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Visualization saved as 'eda_visualization.png'")

def data_quality_check(data):
    """Check for data quality issues"""
    print("\n" + "="*60)
    print("DATA QUALITY ASSESSMENT")
    print("="*60)
    
    issues = []
    
    # Check for empty conversations
    empty_convs = sum(1 for conv in data if len(conv['messages']) == 0)
    if empty_convs > 0:
        issues.append(f"Found {empty_convs} empty conversations")
    
    # Check for messages without content
    empty_messages = 0
    very_short_messages = 0
    missing_roles = 0
    
    for conv in data:
        for msg in conv['messages']:
            if 'content' not in msg or not msg['content']:
                empty_messages += 1
            elif len(msg['content'].strip()) < 3:
                very_short_messages += 1
            
            if 'role' not in msg:
                missing_roles += 1
    
    if empty_messages > 0:
        issues.append(f"Found {empty_messages} messages with no content")
    if very_short_messages > 0:
        issues.append(f"Found {very_short_messages} messages with <3 characters")
    if missing_roles > 0:
        issues.append(f"Found {missing_roles} messages without role")
    
    # Check role consistency
    valid_roles = {'user', 'assistant', 'system'}
    invalid_roles = set()
    
    for conv in data:
        for msg in conv['messages']:
            if msg.get('role') not in valid_roles:
                invalid_roles.add(msg.get('role'))
    
    if invalid_roles:
        issues.append(f"Found invalid roles: {invalid_roles}")
    
    # Check for potential encoding issues
    encoding_issues = 0
    for conv in data:
        for msg in conv['messages']:
            content = msg.get('content', '')
            if '�' in content or '\ufffd' in content:
                encoding_issues += 1
    
    if encoding_issues > 0:
        issues.append(f"Found {encoding_issues} messages with potential encoding issues")
    
    if issues:
        print("⚠️  Data quality issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✅ No major data quality issues found!")
    
    return issues

def training_recommendations(data, stats, content_data):
    """Generate recommendations for training"""
    print("\n" + "="*60)
    print("TRAINING RECOMMENDATIONS")
    print("="*60)
    
    avg_msg_length = np.mean(content_data['char_counts'])
    max_msg_length = max(content_data['char_counts'])
    p95_length = np.percentile(content_data['char_counts'], 95)
    
    print(f"📊 Dataset Summary:")
    print(f"  - {stats['total_conversations']:,} conversations")
    print(f"  - {stats['total_messages']:,} total messages")
    print(f"  - Average message length: {avg_msg_length:.1f} characters")
    print(f"  - 95th percentile length: {p95_length:.1f} characters")
    
    print(f"\n💡 Recommendations:")
    
    # Token length recommendations
    estimated_tokens = avg_msg_length / 4  # Rough estimate: 4 chars per token
    print(f"  - Estimated average tokens per message: ~{estimated_tokens:.0f}")
    print(f"  - Consider max sequence length: {int(p95_length/4) + 50} tokens")
    
    # Batch size recommendations
    if stats['total_conversations'] < 1000:
        print(f"  - Small dataset: Consider batch size 4-8")
    elif stats['total_conversations'] < 10000:
        print(f"  - Medium dataset: Consider batch size 8-16")
    else:
        print(f"  - Large dataset: Consider batch size 16-32")
    
    # Training considerations
    avg_conv_length = np.mean(stats['msg_counts'])
    if avg_conv_length < 3:
        print(f"  - Short conversations: Focus on single-turn quality")
    else:
        print(f"  - Multi-turn conversations: Focus on context preservation")
    
    print(f"  - Consider gradient accumulation if memory is limited")
    print(f"  - Monitor for overfitting with this dataset size")

def main():
    """Main EDA execution function"""
    print("🔍 Starting Exploratory Data Analysis for SFT Training Data")
    print("=" * 70)
    
    # Load data
    data_path = "/home/anselmlong/Projects/almost-anselm/almost-anselm/data/processed/sft_train_new.json"
    data = load_data(data_path)
    
    if data is None:
        return
    
    # Run analyses
    stats = basic_statistics(data)
    role_data = role_analysis(data)
    content_data = content_analysis(data)
    patterns = conversation_patterns(data)
    lang_analysis = language_analysis(data)
    
    # Quality check
    data_quality_check(data)
    
    # Generate visualizations
    create_visualizations(stats, role_data, content_data)
    
    # Training recommendations
    training_recommendations(data, stats, content_data)
    
    print(f"\n✅ EDA Complete! Check the generated visualization and summary above.")

if __name__ == "__main__":
    main()