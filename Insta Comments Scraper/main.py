

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



    
    