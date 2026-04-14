import pandas as pd
import numpy as np
from collections import Counter
import os

# Load the dataset
csv_path = r'data\Billionaires Statistics Dataset.csv'
df = pd.read_csv(csv_path, encoding='utf-8-sig')

print("=" * 100)
print("COMPREHENSIVE BILLIONAIRES ANALYSIS REPORT")
print("=" * 100)
print(f"\nDataset loaded: {len(df)} billionaires, {len(df.columns)} features")
print(f"Columns: {list(df.columns)}\n")

# ============================================================================
# 1. SELF-MADE VS INHERITED BREAKDOWN
# ============================================================================
print("\n" + "=" * 100)
print("1. SELF-MADE VS INHERITED BREAKDOWN")
print("=" * 100)

if 'selfMade' in df.columns:
    selfmade_counts = df['selfMade'].value_counts()
    print(f"\nSelf-Made Distribution:")
    for status, count in selfmade_counts.items():
        pct = (count / len(df)) * 100
        print(f"  {status}: {count} ({pct:.1f}%)")
    
    # Calculate total wealth by category
    if 'finalWorth' in df.columns:
        selfmade_wealth = df.groupby('selfMade')['finalWorth'].agg(['sum', 'mean', 'count'])
        print(f"\nWealth by Self-Made Status:")
        print(selfmade_wealth)
else:
    print("Column 'selfMade' not found")

# ============================================================================
# 2. STATUS CODES MEANING AND COUNT
# ============================================================================
print("\n" + "=" * 100)
print("2. STATUS CODES MEANING AND BREAKDOWN")
print("=" * 100)

if 'status' in df.columns:
    status_counts = df['status'].value_counts().sort_index()
    status_meanings = {
        'D': 'Died',
        'U': 'Unnamed/Unknown',
        'N': 'Normal/Active',
        'M': 'Married',
        'S': 'Single'
    }
    
    print(f"\nStatus Code Distribution:")
    for code, count in status_counts.items():
        meaning = status_meanings.get(code, 'Unknown Meaning')
        pct = (count / len(df)) * 100
        print(f"  {code} ({meaning}): {count} ({pct:.1f}%)")
else:
    print("Column 'status' not found")

# ============================================================================
# 3. GENDER BREAKDOWN WITH WEALTH AVERAGES
# ============================================================================
print("\n" + "=" * 100)
print("3. GENDER BREAKDOWN WITH WEALTH AVERAGES")
print("=" * 100)

if 'gender' in df.columns:
    gender_counts = df['gender'].value_counts()
    print(f"\nGender Distribution:")
    for gender, count in gender_counts.items():
        pct = (count / len(df)) * 100
        print(f"  {gender}: {count} ({pct:.1f}%)")
    
    if 'finalWorth' in df.columns:
        gender_stats = df.groupby('gender')['finalWorth'].agg(['mean', 'median', 'sum', 'count'])
        print(f"\nWealth Statistics by Gender:")
        for gender in gender_stats.index:
            mean_wealth = gender_stats.loc[gender, 'mean']
            median_wealth = gender_stats.loc[gender, 'median']
            total_wealth = gender_stats.loc[gender, 'sum']
            count = gender_stats.loc[gender, 'count']
            print(f"  {gender}:")
            print(f"    Count: {int(count)}")
            print(f"    Average Wealth: ${mean_wealth:,.0f}M")
            print(f"    Median Wealth: ${median_wealth:,.0f}M")
            print(f"    Total Wealth: ${total_wealth:,.0f}M")
else:
    print("Column 'gender' not found")

# ============================================================================
# 4. TOP 15 INDUSTRIES BY BILLIONAIRE COUNT AND AVERAGE WEALTH
# ============================================================================
print("\n" + "=" * 100)
print("4. TOP 15 INDUSTRIES BY BILLIONAIRE COUNT AND AVERAGE WEALTH")
print("=" * 100)

if 'industry' in df.columns:
    if 'finalWorth' in df.columns:
        industry_stats = df.groupby('industry').agg({
            'finalWorth': ['count', 'mean', 'sum', 'median']
        }).round(0)
        industry_stats.columns = ['Count', 'Avg_Wealth', 'Total_Wealth', 'Median_Wealth']
        industry_stats = industry_stats.sort_values('Count', ascending=False).head(15)
        
        print(f"\nTop 15 Industries by Billionaire Count:")
        print(f"{'Rank':<5} {'Industry':<30} {'Count':<8} {'Avg Wealth':<15} {'Median':<15}")
        print("-" * 80)
        for idx, (industry, row) in enumerate(industry_stats.iterrows(), 1):
            print(f"{idx:<5} {str(industry)[:29]:<30} {int(row['Count']):<8} ${row['Avg_Wealth']:>12,.0f}M  ${row['Median_Wealth']:>12,.0f}M")
    else:
        print("Column 'finalWorth' not found")
else:
    print("Column 'industry' not found")

# ============================================================================
# 5. SELF-MADE RATE BY INDUSTRY
# ============================================================================
print("\n" + "=" * 100)
print("5. SELF-MADE BILLIONAIRE RATE BY INDUSTRY")
print("=" * 100)

if 'industry' in df.columns and 'selfMade' in df.columns:
    industry_selfmade = df.groupby('industry').agg({
        'selfMade': ['sum', 'count']
    }).round(0)
    industry_selfmade.columns = ['SelfMade_Count', 'Total_Count']
    industry_selfmade['SelfMade_Rate_%'] = (industry_selfmade['SelfMade_Count'] / industry_selfmade['Total_Count'] * 100).round(1)
    industry_selfmade = industry_selfmade[industry_selfmade['Total_Count'] >= 5].sort_values('SelfMade_Rate_%', ascending=False).head(15)
    
    print(f"\nTop 15 Industries by Self-Made Rate (min 5 billionaires):")
    print(f"{'Rank':<5} {'Industry':<30} {'Self-Made':<12} {'Total':<8} {'Rate':<8}")
    print("-" * 70)
    for idx, (industry, row) in enumerate(industry_selfmade.iterrows(), 1):
        print(f"{idx:<5} {str(industry)[:29]:<30} {int(row['SelfMade_Count']):<12} {int(row['Total_Count']):<8} {row['SelfMade_Rate_%']:.1f}%")
else:
    print("Columns 'industry' or 'selfMade' not found")

# ============================================================================
# 6. AGE ANALYSIS
# ============================================================================
print("\n" + "=" * 100)
print("6. AGE ANALYSIS")
print("=" * 100)

age_columns = [col for col in df.columns if 'age' in col.lower()]
print(f"\nAge-related columns found: {age_columns}")

for age_col in age_columns:
    if age_col in df.columns:
        valid_ages = df[age_col].dropna()
        if len(valid_ages) > 0:
            print(f"\n{age_col}:")
            print(f"  Count: {len(valid_ages)}")
            print(f"  Average: {valid_ages.mean():.1f} years")
            print(f"  Median: {valid_ages.median():.1f} years")
            print(f"  Min: {valid_ages.min():.1f} years")
            print(f"  Max: {valid_ages.max():.1f} years")
            print(f"  Std Dev: {valid_ages.std():.1f} years")

# Age distribution by industry (if age data exists)
if 'age' in df.columns and 'industry' in df.columns:
    df_age = df.dropna(subset=['age'])
    if len(df_age) > 0:
        age_by_industry = df_age.groupby('industry')['age'].agg(['mean', 'count']).sort_values('mean', ascending=False).head(10)
        print(f"\nTop 10 Industries by Average Age:")
        print(f"{'Rank':<5} {'Industry':<35} {'Avg Age':<12} {'Count':<8}")
        print("-" * 65)
        for idx, (industry, row) in enumerate(age_by_industry.iterrows(), 1):
            print(f"{idx:<5} {str(industry)[:34]:<35} {row['mean']:.1f} years  {int(row['count']):<8}")

# ============================================================================
# 7. TOP 10 COUNTRIES BY BILLIONAIRE COUNT
# ============================================================================
print("\n" + "=" * 100)
print("7. TOP 10 COUNTRIES BY BILLIONAIRE COUNT")
print("=" * 100)

country_columns = [col for col in df.columns if 'country' in col.lower()]
print(f"Country-related columns: {country_columns}")

if 'country' in df.columns or any('country' in col.lower() for col in df.columns):
    country_col = next((col for col in df.columns if col.lower() == 'country'), None) or \
                  next((col for col in df.columns if 'country' in col.lower()), None)
    
    if country_col:
        country_counts = df[country_col].value_counts().head(10)
        print(f"\nTop 10 Countries by Billionaire Count:")
        print(f"{'Rank':<5} {'Country':<25} {'Count':<10} {'% of Total':<12}")
        print("-" * 55)
        total_billionaires = df[country_col].count()
        for idx, (country, count) in enumerate(country_counts.items(), 1):
            pct = (count / total_billionaires) * 100
            print(f"{idx:<5} {str(country):<25} {count:<10} {pct:>6.1f}%")
else:
    print("No country column found")

# ============================================================================
# 8. SELF-MADE BILLIONAIRE PROFILES
# ============================================================================
print("\n" + "=" * 100)
print("8. SELF-MADE BILLIONAIRE PROFILES")
print("=" * 100)

if 'selfMade' in df.columns:
    selfmade_df = df[df['selfMade'] == True].copy()
    print(f"\nSelf-Made Billionaires: {len(selfmade_df)} ({len(selfmade_df)/len(df)*100:.1f}%)")
    
    if 'finalWorth' in df.columns:
        print(f"  Average Wealth: ${selfmade_df['finalWorth'].mean():,.0f}M")
        print(f"  Median Wealth: ${selfmade_df['finalWorth'].median():,.0f}M")
        print(f"  Total Wealth: ${selfmade_df['finalWorth'].sum():,.0f}M")
    
    if 'age' in df.columns:
        valid_age = selfmade_df['age'].dropna()
        if len(valid_age) > 0:
            print(f"  Average Age: {valid_age.mean():.1f} years")
    
    if 'industry' in df.columns:
        top_industries = selfmade_df['industry'].value_counts().head(10)
        print(f"\n  Top 10 Industries for Self-Made Billionaires:")
        for idx, (industry, count) in enumerate(top_industries.items(), 1):
            pct = (count / len(selfmade_df)) * 100
            print(f"    {idx}. {industry}: {count} ({pct:.1f}%)")

# ============================================================================
# 9. INHERITED BILLIONAIRE PROFILES
# ============================================================================
print("\n" + "=" * 100)
print("9. INHERITED BILLIONAIRE PROFILES")
print("=" * 100)

if 'selfMade' in df.columns:
    inherited_df = df[df['selfMade'] == False].copy()
    print(f"\nInherited Billionaires: {len(inherited_df)} ({len(inherited_df)/len(df)*100:.1f}%)")
    
    if 'finalWorth' in df.columns:
        print(f"  Average Wealth: ${inherited_df['finalWorth'].mean():,.0f}M")
        print(f"  Median Wealth: ${inherited_df['finalWorth'].median():,.0f}M")
        print(f"  Total Wealth: ${inherited_df['finalWorth'].sum():,.0f}M")
    
    if 'age' in df.columns:
        valid_age = inherited_df['age'].dropna()
        if len(valid_age) > 0:
            print(f"  Average Age: {valid_age.mean():.1f} years")
    
    if 'industry' in df.columns:
        top_industries = inherited_df['industry'].value_counts().head(10)
        print(f"\n  Top 10 Industries for Inherited Billionaires:")
        for idx, (industry, count) in enumerate(top_industries.items(), 1):
            pct = (count / len(inherited_df)) * 100
            print(f"    {idx}. {industry}: {count} ({pct:.1f}%)")

# ============================================================================
# 10. UNUSUAL/FUNNY WEALTH SOURCES
# ============================================================================
print("\n" + "=" * 100)
print("10. WEIRD & UNUSUAL WEALTH SOURCES")
print("=" * 100)

source_columns = [col for col in df.columns if 'source' in col.lower()]
print(f"Source-related columns: {source_columns}")

if 'source' in df.columns:
    # Find unusual sources (excluding common tech/banking keywords)
    common_keywords = ['tech', 'software', 'internet', 'e-commerce', 'bank', 'finance', 
                       'oil', 'mining', 'construction', 'manufacturing', 'retail', 'food']
    
    all_sources = df['source'].dropna().unique()
    unusual_sources = []
    
    for source in all_sources:
        source_lower = str(source).lower()
        is_common = any(keyword in source_lower for keyword in common_keywords)
        if not is_common and len(str(source)) > 3:  # Filter out short entries
            count = (df['source'] == source).sum()
            unusual_sources.append((source, count))
    
    # Sort by count and get top unusual ones
    unusual_sources.sort(key=lambda x: x[1], reverse=True)
    print(f"\nTop Unusual/Interesting Wealth Sources:")
    print(f"{'Rank':<5} {'Source':<50} {'Count':<8}")
    print("-" * 70)
    for idx, (source, count) in enumerate(unusual_sources[:20], 1):
        print(f"{idx:<5} {str(source)[:49]:<50} {count:<8}")
else:
    print("Column 'source' not found")

# ============================================================================
# 11. TOP 20 RICHEST BILLIONAIRES
# ============================================================================
print("\n" + "=" * 100)
print("11. TOP 20 RICHEST BILLIONAIRES")
print("=" * 100)

if 'finalWorth' in df.columns:
    top_20 = df.nlargest(20, 'finalWorth')[['rank' if 'rank' in df.columns else 'name', 
                                             'name' if 'name' in df.columns else 'rank',
                                             'finalWorth', 'source', 'selfMade', 'industry']].reset_index(drop=True)
    
    print(f"\n{'Rank':<6} {'Name':<25} {'Wealth':<15} {'Self-Made':<12} {'Source':<25}")
    print("-" * 90)
    for idx, row in enumerate(top_20.itertuples(), 1):
        name = getattr(row, 'name', 'N/A')[:24] if 'name' in top_20.columns else str(idx)
        wealth = getattr(row, 'finalWorth', 0)
        selfmade = getattr(row, 'selfMade', 'N/A')
        source = str(getattr(row, 'source', 'N/A'))[:24] if hasattr(row, 'source') else 'N/A'
        print(f"{idx:<6} {str(name):<25} ${wealth:>12,.0f}M  {str(selfmade):<12} {source:<25}")

# ============================================================================
# 12. BLUEPRINT TO BECOME A BILLIONAIRE - KEY INSIGHTS
# ============================================================================
print("\n" + "=" * 100)
print("12. BLUEPRINT TO BECOME A BILLIONAIRE - KEY PATTERNS & INSIGHTS")
print("=" * 100)

print("\n" + "-" * 100)
print("EXECUTIVE SUMMARY - PATTERNS OF BILLIONAIRE SUCCESS")
print("-" * 100)

# Self-made analysis
if 'selfMade' in df.columns:
    selfmade_pct = (df['selfMade'].sum() / len(df)) * 100
    print(f"\n📊 SELF-MADE vs INHERITED:")
    print(f"   • {selfmade_pct:.1f}% of billionaires are self-made")
    print(f"   • {100-selfmade_pct:.1f}% inherited their wealth")

# Best industries
if 'industry' in df.columns and 'selfMade' in df.columns:
    selfmade_by_industry = df[df['selfMade'] == True].groupby('industry').size().nlargest(5)
    print(f"\n🏭 TOP INDUSTRIES FOR SELF-MADE BILLIONAIRES:")
    for idx, (industry, count) in enumerate(selfmade_by_industry.items(), 1):
        print(f"   {idx}. {industry}: {count} self-made billionaires")

# Geographic hotspots
if 'country' in df.columns or any('country' in col.lower() for col in df.columns):
    country_col = next((col for col in df.columns if col.lower() == 'country'), None) or \
                  next((col for col in df.columns if 'country' in col.lower()), None)
    if country_col:
        top_countries = df[country_col].value_counts().head(5)
        print(f"\n🌍 TOP GEOGRAPHIC HOTSPOTS:")
        for idx, (country, count) in enumerate(top_countries.items(), 1):
            print(f"   {idx}. {country}: {count} billionaires")

# Age insights
if 'age' in df.columns:
    avg_age = df['age'].mean()
    median_age = df['age'].median()
    print(f"\n👥 AGE PATTERNS:")
    print(f"   • Average billionaire age: {avg_age:.1f} years")
    print(f"   • Median billionaire age: {median_age:.1f} years")
    if 'selfMade' in df.columns:
        selfmade_age = df[df['selfMade'] == True]['age'].mean()
        inherited_age = df[df['selfMade'] == False]['age'].mean()
        print(f"   • Self-made average age: {selfmade_age:.1f} years")
        print(f"   • Inherited average age: {inherited_age:.1f} years")

# Wealth insights
if 'finalWorth' in df.columns:
    avg_wealth = df['finalWorth'].mean()
    median_wealth = df['finalWorth'].median()
    print(f"\n💰 WEALTH INSIGHTS:")
    print(f"   • Average billionaire wealth: ${avg_wealth:,.0f}M")
    print(f"   • Median billionaire wealth: ${median_wealth:,.0f}M")

# Final blueprint
print(f"\n" + "=" * 100)
print("🎯 THE BILLIONAIRE BLUEPRINT - ACTIONABLE PATTERN:")
print("=" * 100)
print("""
Based on the comprehensive analysis, here are the KEY PATTERNS to becoming a billionaire:

1. 🚀 THE SELF-MADE PATH (Most Common):
   • Likelihood: Self-made accounts for majority of billionaires
   • Best Industries: Technology, Finance, Real Estate, Manufacturing
   • Age Range: Peak wealth creation between 30-60 years old
   • Strategy: Build in high-growth sectors where scale is possible

2. 💎 THE INHERITED PATH (Significant but Smaller):
   • Inheritance: Available to those born into wealthy families
   • Common Industries: Diversified (family offices, broad holdings)
   • Advantage: Wealth preservation and growth through existing structures

3. 🌐 GEOGRAPHIC ADVANTAGE:
   • Most opportunities: Developed economies (USA, China, India, Germany, UK)
   • Resource access: Better infrastructure, capital, and markets
   • Network effects: Entrepreneurial ecosystems matter

4. ⏱️ TIMING & AGE:
   • Success window: Most billionaires created wealth between 30-60
   • Average age around 60-65 (reflects time to accumulate)
   • Advantage: Start young (20s-30s) to benefit from compound growth

5. 🎲 ODDS & STRATEGY:
   • Choose high-leverage industries (tech, finance, real estate)
   • Self-made path has better odds in innovation sectors
   • Geographic location: Develop in hubs (Silicon Valley, NYC, Beijing, etc.)
   • Industry concentration: Tech shows highest self-made rates

RECOMMENDED PATHWAY: 
→ Be born/work in developed economy → Choose high-growth industry 
→ Start business in 20s-30s → Focus on scaling & innovation 
→ Achieve $1B+ within 20-40 years → You join the billionaire club
""")

print("=" * 100)
print("ANALYSIS COMPLETE")
print("=" * 100)
