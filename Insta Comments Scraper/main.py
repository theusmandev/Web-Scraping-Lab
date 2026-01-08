

import instaloader
import csv
import time

def scrape_anonymous():
    print("\n--- 🕵️ Anonymous Scraper (No Login) ---\n")
    
    # Koi login nahi, bas simple loader
    L = instaloader.Instaloader()

    # Post Shortcode (URL se: DSsGIk4CF2K)
    shortcode = "DSsGIk4CF2K"

    try:
        print(f"⏳ Fetching Post {shortcode} anonymously...")
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        print(f"📝 Owner: {post.owner_username}")
        print(f"💬 Total Comments: {post.comments}")
        print("\n⬇️ Scraping Started...\n")

        comments_data = []
        count = 0

        for comment in post.get_comments():
            comments_data.append({
                "username": comment.owner.username,
                "text": comment.text
            })
            count += 1
            print(f"[{count}] {comment.owner.username}: {comment.text[:30]}")

            # Bohot slow speed taake pakre na jayen
            if count % 20 == 0:
                print("⏳ Sleeping 5 seconds...")
                time.sleep(5)

        # Save
        filename = f"comments_{shortcode}_anon.csv"
        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["username", "text"])
            writer.writeheader()
            writer.writerows(comments_data)

        print(f"\n✅ DONE! {count} comments saved.")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nNateja: Agar ye fail hua, to Instagram ne apka IP Address block kar dia ha.")

if __name__ == "__main__":
    scrape_anonymous()
    
    
    
    
    
    
    
# import instaloader
# import csv
# import time
# import re
# from http.cookies import SimpleCookie

# def scrape_with_full_cookies():
#     print("\n--- 🍪 Instagram Full Cookie Scraper ---\n")

#     # 1. Setup Instaloader (Updated User Agent)
#     # Hum bilkul real browser ban kar jayenge
#     L = instaloader.Instaloader(
#         max_connection_attempts=3,
#         user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
#     )

#     # 2. Ask for FULL Cookie String
#     print("Instruction: Network Tab > Request Headers > 'Cookie' ki puri value copy karein.")
#     cookie_string = input("👉 Paste Full Cookie String here: ").strip()

#     # 3. Parse and Inject Cookies
#     try:
#         # Cookie string ko dictionary ma convert karna
#         cookie_obj = SimpleCookie()
#         cookie_obj.load(cookie_string)
        
#         cookies_dict = {}
#         for key, morsel in cookie_obj.items():
#             cookies_dict[key] = morsel.value
            
#         # Instaloader ma inject karna
#         L.context._session.cookies.update(cookies_dict)
        
#         # Verify
#         username = L.test_login()
#         if username:
#             print(f"✅ Login & Tokens Verified! User: {username}")
#         else:
#             print("⚠️ Warning: Login confirm nahi hua, lekin try kartay hain.")

#     except Exception as e:
#         print(f"❌ Cookie Error: {e}")
#         return

#     # 4. Post URL
#     post_url = input("\n🔗 Post URL dalein: ").strip()
    
#     match = re.search(r"/p/([a-zA-Z0-9_-]+)", post_url)
#     if not match:
#         print("❌ Invalid URL")
#         return
#     shortcode = match.group(1)

#     try:
#         print(f"\n⏳ Fetching Post {shortcode}...")
#         post = instaloader.Post.from_shortcode(L.context, shortcode)
        
#         print(f"📝 Owner: {post.owner_username}")
#         print(f"💬 Total Comments: {post.comments}")
#         print("\n⬇️ Scraping Started...\n")

#         comments_data = []
#         count = 0

#         # Loop through comments
#         for comment in post.get_comments():
#             comments_data.append({
#                 "username": comment.owner.username,
#                 "text": comment.text,
#                 "timestamp": comment.created_at_utc.strftime("%Y-%m-%d %H:%M:%S")
#             })
#             count += 1
            
#             # Print clean output
#             clean_text = comment.text[:30].replace('\n', ' ')
#             print(f"[{count}] {comment.owner.username}: {clean_text}")

#             # --- Rate Limit Safety ---
#             # Har 30 comments ke baad 5 second ka break
#             if count % 30 == 0:
#                 print("⏳ Sleeping 5 seconds (Safety)...")
#                 time.sleep(5)

#         # Save File
#         filename = f"comments_{shortcode}_full.csv"
#         with open(filename, "w", newline="", encoding="utf-8-sig") as f:
#             writer = csv.DictWriter(f, fieldnames=["username", "text", "timestamp"])
#             writer.writeheader()
#             writer.writerows(comments_data)

#         print(f"\n✅ DONE! {count} comments saved.")
#         print(f"📁 File: {filename}")

#     except Exception as e:
#         print(f"\n❌ Error: {e}")
#         if "Login required" in str(e):
#             print("💡 Cookie expire ho gayi ha ya 'csrftoken' missing ha.")

#     input("\nPress Enter to exit...")

# if __name__ == "__main__":
#     scrape_with_full_cookies()





# import instaloader
# import csv
# import time
# import re

# def scrape_comments_via_session():
#     print("\n--- 🛡️ Instagram Session ID Scraper (Fixed) ---\n")

#     # 1. Setup Instaloader
#     L = instaloader.Instaloader(
#         max_connection_attempts=3,
#         user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#     )

#     # 2. Ask for Session ID
#     print("Humein Login nahi karna, direct Browser ki ID use karni ha.")
#     session_id = input("👉 Apni 'sessionid' paste karein: ").strip()

#     # 3. Inject Session ID (Updated Code)
#     try:
#         L.context._session.cookies.set('sessionid', session_id)
        
#         # Test karein ke session theek ha ya nahi
#         print("🔄 Session check ho raha ha...")
#         username = L.test_login()
        
#         if username:
#             print(f"✅ Login Confirmed! User: {username}")
#         else:
#             print("⚠️ Session inject hua lekin username confirm nahi hua. Phir bhi try kartay hain.")

#     except Exception as e:
#         print(f"❌ Session Error: {e}")
#         print("Tip: Session ID dobara copy karein, shayad ghalat copy hui ha.")
#         return

#     # 4. Ask for Post URL
#     post_url = input("\n🔗 Post URL dalein: ").strip()
    
#     # Extract Shortcode
#     match = re.search(r"/p/([a-zA-Z0-9_-]+)", post_url)
#     if not match:
#         print("❌ Invalid URL")
#         return
#     shortcode = match.group(1)

#     try:
#         print(f"\n⏳ Fetching Post {shortcode}...")
#         post = instaloader.Post.from_shortcode(L.context, shortcode)
        
#         print(f"📝 Owner: {post.owner_username}")
#         print(f"💬 Comments Count: {post.comments}")
#         print("\n⬇️ Scraping Started...\n")

#         comments_data = []
#         count = 0

#         for comment in post.get_comments():
#             comments_data.append({
#                 "username": comment.owner.username,
#                 "text": comment.text,
#                 "timestamp": comment.created_at_utc.strftime("%Y-%m-%d %H:%M:%S")
#             })
#             count += 1
#             print(f"[{count}] {comment.owner.username}: {comment.text[:30].replace('\n', ' ')}")

#             # Thora sa break (Anti-ban)
#             if count % 40 == 0:
#                 print("⏸️ Thora sa break (Anti-ban)...")
#                 time.sleep(4)

#         # Save File
#         filename = f"comments_{shortcode}_safe.csv"
#         with open(filename, "w", newline="", encoding="utf-8-sig") as f:
#             writer = csv.DictWriter(f, fieldnames=["username", "text", "timestamp"])
#             writer.writeheader()
#             writer.writerows(comments_data)

#         print(f"\n✅ MUBARAK HO! {count} comments save ho gaye.")
#         print(f"📁 File: {filename}")

#     except Exception as e:
#         print(f"\n❌ Error: {e}")
#         print("💡 Agar 'Redirect' ya 'Login Required' aye, to Session ID expire ho chuki ha.")

#     input("\nPress Enter to exit...")

# if __name__ == "__main__":
#     scrape_comments_via_session()







# import instaloader
# import csv
# import time
# import re
# import os
# import random

# def get_shortcode_from_url(url):
#     """Extracts shortcode from various URL formats."""
#     match = re.search(r"/p/([a-zA-Z0-9_-]+)", url)
#     if match:
#         return match.group(1)
#     # Handle Reel URLs just in case
#     match = re.search(r"/reel/([a-zA-Z0-9_-]+)", url)
#     if match:
#         return match.group(1)
#     raise ValueError("Could not extract shortcode. Check URL format.")

# def login_instagram(L, username):
#     """Handles Login, Session Files, and 2FA."""
#     session_file = f"session-{username}"

#     # 1. Try loading existing session
#     if os.path.exists(session_file):
#         try:
#             print(f"🔄 Loading session for {username}...")
#             L.load_session_from_file(username, filename=session_file)
#             print("✅ Session Loaded! (No password needed)")
#             return True
#         except Exception as e:
#             print(f"⚠️ Session file corrupt or expired: {e}")

#     # 2. If no session, perform manual login
#     try:
#         password = input(f"🔑 Enter Password for {username}: ")
#         L.login(username, password)
#         print("✅ Login Successful!")
#     except instaloader.TwoFactorAuthRequiredException:
#         # Handle 2FA
#         code = input("🛡️ 2FA Required! Enter Code from SMS/App: ")
#         L.two_factor_login(code)
#         print("✅ 2FA Verified!")
#     except Exception as e:
#         print(f"❌ Login Failed: {e}")
#         return False

#     # 3. Save session for next time
#     try:
#         L.save_session_to_file(filename=session_file)
#         print(f"💾 Session saved to '{session_file}' (Don't delete this file!)")
#     except Exception as e:
#         print(f"⚠️ Could not save session: {e}")

#     return True

# def scrape_comments():
#     print("\n--- 🚀 Ultimate Instagram Comment Scraper ---\n")

#     # Setup Instaloader
#     L = instaloader.Instaloader(
#         sleep=True,             # Random sleep between requests
#         user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#         max_connection_attempts=3
#     )

#     # Login Phase
#     username = input("👤 Enter Your Instagram Username: ")
#     if not login_instagram(L, username):
#         input("\nPress Enter to exit...")
#         return

#     # Input Target URL
#     post_url = input("\n🔗 Enter Post URL: ").strip()

#     try:
#         shortcode = get_shortcode_from_url(post_url)
#         print(f"📍 Target Shortcode: {shortcode}")
        
#         print("⏳ Fetching Post Metadata...")
#         post = instaloader.Post.from_shortcode(L.context, shortcode)
#         print(f"📝 Post Owner: {post.owner_username}")
#         print(f"💬 Estimated Comments: {post.comments}")
        
#         print("\n⬇️  Scraping Started...\n")

#         comments_data = []
#         count = 0
        
#         # Scrape Loop
#         for comment in post.get_comments():
#             comments_data.append({
#                 "username": comment.owner.username,
#                 "text": comment.text,
#                 "timestamp": comment.created_at_utc.strftime("%Y-%m-%d %H:%M:%S"),
#                 "likes": comment.likes_count
#             })
            
#             count += 1
#             print(f"[{count}] {comment.owner.username}: {comment.text[:30].replace('\n', ' ')}...")

#             # --- SAFETY DELAYS ---
#             # Sleep every 50 comments to look human
#             if count % 50 == 0:
#                 sleep_time = random.randint(5, 10)
#                 print(f"⏸️  Sleeping for {sleep_time} seconds (Safety)...")
#                 time.sleep(sleep_time)

#         # Save to CSV
#         filename = f"comments_{shortcode}.csv"
#         print(f"\n💾 Saving to {filename}...")
        
#         # 'utf-8-sig' ensures Excel reads Urdu/Emojis correctly
#         with open(filename, "w", newline="", encoding="utf-8-sig") as f:
#             writer = csv.DictWriter(
#                 f, 
#                 fieldnames=["username", "text", "timestamp", "likes"]
#             )
#             writer.writeheader()
#             writer.writerows(comments_data)

#         print(f"\n✅ SUCCESS! {count} comments saved.")

#     except instaloader.ConnectionException as e:
#         print(f"\n❌ Connection Error: {e}")
#     except instaloader.QueryReturnedNotFoundException:
#         print("\n❌ Post not found (Check URL or if account is Private).")
#     except Exception as e:
#         print(f"\n❌ Unexpected Error: {e}")

#     input("\nPress Enter to close...")

# if __name__ == "__main__":
#     scrape_comments()




#okay but this was me challange on insta

# import instaloader
# import csv
# import time
# import re

# def extract_shortcode(url):
#     match = re.search(r"/p/([^/]+)/", url)
#     if not match:
#         raise ValueError("Invalid Instagram Post URL")
#     return match.group(1)

# def scrape_comments():
#     print("\n--- Instagram Comment Scraper (Local PC) ---\n")

#     # 1️⃣ Setup Instaloader
#     L = instaloader.Instaloader(
#         sleep=True,
#         quiet=False,
#         max_connection_attempts=3
#     )

#     # 2️⃣ Login (NO getpass – Enter issue fixed)
#     username = input("Enter Instagram Username: ")
#     password = input("Enter Instagram Password (typing visible): ")

#     try:
#         print("\nLogging in...")
#         L.login(username, password)
#         print("✅ Login Successful!\n")
#     except Exception as e:
#         print(f"❌ Login Failed: {e}")
#         input("\nPress Enter to exit...")
#         return

#     # 3️⃣ Post URL input
#     post_url = input("Enter Instagram Post URL: ")

#     try:
#         shortcode = extract_shortcode(post_url)
#     except Exception as e:
#         print(f"❌ {e}")
#         input("\nPress Enter to exit...")
#         return

#     # 4️⃣ Fetch post
#     try:
#         print("\nFetching post...")
#         post = instaloader.Post.from_shortcode(L.context, shortcode)

#         print(f"Post Owner : {post.owner_username}")
#         print(f"Comments   : ~{post.comments}")
#         print("\nScraping started...\n")

#         comments_data = []
#         count = 0

#         # 5️⃣ Scrape comments
#         for comment in post.get_comments():
#             comments_data.append({
#                 "username": comment.owner.username,
#                 "text": comment.text,
#                 "timestamp": comment.created_at_utc.strftime("%Y-%m-%d %H:%M:%S")
#             })

#             count += 1
#             print(f"[{count}] {comment.owner.username}: {comment.text[:40]}")

#             # Rate limit safety
#             if count % 40 == 0:
#                 print("⏸ Sleeping 4 seconds...")
#                 time.sleep(4)

#         # 6️⃣ Save CSV
#         filename = f"comments_{shortcode}.csv"
#         with open(filename, "w", newline="", encoding="utf-8-sig") as f:
#             writer = csv.DictWriter(
#                 f,
#                 fieldnames=["username", "text", "timestamp"]
#             )
#             writer.writeheader()
#             writer.writerows(comments_data)

#         print(f"\n✅ DONE!")
#         print(f"Total Comments Saved: {count}")
#         print(f"File Name: {filename}")

#     except Exception as e:
#         print(f"\n❌ Error: {e}")
#         print("⚠️ Instagram rate limit ya private post ho sakta hai")

#     input("\nPress Enter to exit...")

# if __name__ == "__main__":
#     scrape_comments()











# import instaloader
# import csv
# import time
# import re
# import os
# from getpass import getpass

# SESSION_FILE = "insta_session"

# def extract_shortcode(url):
#     match = re.search(r"/p/([^/]+)/", url)
#     if not match:
#         raise ValueError("Invalid Instagram post URL")
#     return match.group(1)

# def scrape_comments():
#     L = instaloader.Instaloader(
#         sleep=True,
#         quiet=False,
#         max_connection_attempts=3
#     )

#     print("\n--- Instagram Comment Scraper (Local PC) ---")

#     # ================= LOGIN =================
#     username = input("Enter Instagram Username: ")

#     # Session load (agar pehle login ho chuka ho)
#     try:
#         if os.path.exists(SESSION_FILE):
#             L.load_session_from_file(username, SESSION_FILE)
#             print("✅ Session loaded (No login needed)")
#         else:
#             raise FileNotFoundError
#     except:
#         password = getpass("Enter Password: ")
#         try:
#             L.login(username, password)
#             L.save_session_to_file(SESSION_FILE)
#             print("✅ Login successful & session saved")
#         except instaloader.exceptions.TwoFactorAuthRequiredException:
#             print("❌ 2FA enabled. Please disable temporarily or login once manually.")
#             return
#         except Exception as e:
#             print(f"❌ Login failed: {e}")
#             return

#     # ================= POST INPUT =================
#     post_url = input("\nEnter Instagram Post URL: ").strip()
#     try:
#         shortcode = extract_shortcode(post_url)
#     except Exception as e:
#         print(f"❌ {e}")
#         return

#     # ================= FETCH POST =================
#     try:
#         print("\nFetching post data...")
#         post = instaloader.Post.from_shortcode(L.context, shortcode)

#         print(f"Post Owner : {post.owner_username}")
#         print(f"Comments   : ~{post.comments}")
#         print("Scraping started...\n")

#         comments_data = []
#         count = 0

#         for comment in post.get_comments():
#             comments_data.append({
#                 "username": comment.owner.username,
#                 "text": comment.text,
#                 "timestamp": comment.created_at_utc.strftime("%Y-%m-%d %H:%M:%S")
#             })
#             count += 1

#             print(f"[{count}] {comment.owner.username}: {comment.text[:40]}")

#             # Safe delay
#             if count % 40 == 0:
#                 print("⏸ Sleeping 4 seconds...")
#                 time.sleep(4)

#         # ================= SAVE CSV =================
#         filename = f"comments_{shortcode}.csv"
#         with open(filename, "w", newline="", encoding="utf-8-sig") as f:
#             writer = csv.DictWriter(
#                 f,
#                 fieldnames=["username", "text", "timestamp"]
#             )
#             writer.writeheader()
#             writer.writerows(comments_data)

#         print(f"\n✅ DONE! {count} comments saved")
#         print(f"📁 File: {filename}")

#     except Exception as e:
#         print(f"\n❌ Error: {e}")
#         print("⚠️ Try again after some time (Instagram rate limit)")

# if __name__ == "__main__":
#     scrape_comments()
#     input("\nPress Enter to exit...")


# import instaloader
# import csv
# import time
# from getpass import getpass

# def scrape_comments():
#     # 1. Setup Instaloader
#     L = instaloader.Instaloader()

#     print("--- Instagram Comment Scraper (Local PC) ---")
    
#     # 2. Login Process
#     print("\nStep 1: Login")
#     username = input("Enter Username: ")
#     # getpass se password type kartay waqt nazar nahi ata (Security ke liye)
#     password = getpass("Enter Password: ") 

#     try:
#         print(f"Logging in as {username}...")
#         L.login(username, password)
#         print("Login Successful! ✅")
#     except Exception as e:
#         print(f"\n❌ Login Failed: {e}")
#         if "TwoFactorAuthRequired" in str(e):
#             print("Apne 2FA code enter karein agar console ma maanga jaye.")
#         input("Press Enter to close...")
#         return

#     # 3. Target Post Shortcode
#     # Agar code ma fix rakhna ha to ye use karein:
#     SHORTCODE = "DSsGIk4CF2K" 
    
#     # Agar har baar naya link maangna ha to niche wali line uncomment karein:
#     # SHORTCODE = input("\nEnter Post Shortcode (e.g., DSsGIk4CF2K): ")

#     try:
#         print(f"\nStep 2: Fetching Post {SHORTCODE}...")
#         post = instaloader.Post.from_shortcode(L.context, SHORTCODE)
        
#         print(f"Post Owner: {post.owner_username}")
#         print(f"Total Comments: {post.comments} (Approx)")
#         print("Scraping started... (Please wait) ⏳")

#         comments_data = []
#         count = 0

#         # 4. Loop through comments
#         for comment in post.get_comments():
#             comments_data.append({
#                 "username": comment.owner.username,
#                 "text": comment.text,
#                 "timestamp": str(comment.created_at_utc)
#             })
#             count += 1
            
#             # Console par print karein taake pata chalay script chal rahi ha
#             print(f"[{count}] {comment.owner.username}: {comment.text[:30]}...")
            
#             # 5. Rate Limiting (Important!)
#             # Har 50 comments ke baad 3 second ka break
#             if count % 50 == 0:
#                 print("Sleeping for 3 seconds to avoid block... zzz")
#                 time.sleep(3) 

#         # 6. Save to CSV
#         filename = f"comments_{SHORTCODE}.csv"
        
#         # 'utf-8-sig' zaroori ha taake Excel ma Urdu/Hindi/Emojis theek nazar ayen
#         with open(filename, "w", newline="", encoding="utf-8-sig") as f:
#             writer = csv.DictWriter(f, fieldnames=["username", "text", "timestamp"])
#             writer.writeheader()
#             writer.writerows(comments_data)

#         print(f"\n✅ Success! {count} comments saved.")
#         print(f"File saved as: {filename}")

#     except Exception as e:
#         print(f"\n❌ Error Occurred: {e}")
#         print("Note: Agar '401' ya 'Redirect' error aye to thori dair baad try karein.")

# if __name__ == "__main__":
#     scrape_comments()
#     input("\nPress Enter to exit...")








# import instaloader
# import csv
# import time

# # --- SETUP ---
# L = instaloader.Instaloader()

# # Yahan apni Session ID paste karein
# SESSION_ID = "79984995414%3A3dP54kcbztdIxh%3A16%3AAYgzaR6O0Fp3pPui0ljL_Qo1MTPPsZm-_SqTsG53Jg"

# # Login Bypass using Session ID
# try:
#     L.context._session.cookies.set('sessionid', SESSION_ID)
#     L.context.is_logged_in = True
#     print("Session Loaded Successfully!")
# except Exception as e:
#     print(f"Session Error: {e}")

# # Target Post
# SHORTCODE = "DSsGIk4CF2K"

# try:
#     print(f"Fetching post {SHORTCODE}...")
#     post = instaloader.Post.from_shortcode(L.context, SHORTCODE)
    
#     print(f"Post Owner: {post.owner_username}")
#     print(f"Total Comments: {post.comments}")
#     print("Scraping comments... (Do not close)")

#     comments_data = []
#     count = 0

#     for comment in post.get_comments():
#         comments_data.append({
#             "username": comment.owner.username,
#             "text": comment.text,
#             "timestamp": str(comment.created_at_utc)
#         })
#         count += 1
        
#         # Thora fast print karein gay local pc par
#         print(f"Scraped {count}: {comment.owner.username}")
        
#         # Local PC par delay kam rakh saktay hain (2 seconds)
#         if count % 50 == 0:
#             time.sleep(2) 

#     # Save to CSV
#     filename = f"comments_{SHORTCODE}.csv"
#     with open(filename, "w", newline="", encoding="utf-8") as f:
#         writer = csv.DictWriter(f, fieldnames=["username", "text", "timestamp"])
#         writer.writeheader()
#         writer.writerows(comments_data)

#     print(f"\nDone! File saved as: {filename}")
#     input("Press Enter to exit...")

# except Exception as e:
#     print(f"\nError: {e}")
#     print("Agar 'Login Required' aye, to apko Session ID refresh karni hogi.")
#     input("Press Enter to exit...")
    
    