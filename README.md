# Claude Ship test: three hidden bugs

This is the small test I used in my reel about Claude Ship (Anthropic's `/ship` command in Claude Code). It is a tiny order book for an online shop. One branch adds discount codes, a customer search and invoice due dates, and I hid **three bugs** in that change. All the tests pass with the bugs inside.

Use it to see for yourself how much a code review by Claude catches, and to practice the habit that matters most: **run the review again after every fix.**

## Run the test yourself

```bash
git clone https://github.com/krisuuu2/claude-ship-test.git
cd claude-ship-test
git checkout discounts-and-invoices
python -m pytest        # all 5 tests pass, bugs included
claude
```

Then type `/ship` in Claude Code. If `/ship` is not available for you, type `/code-review high`, because that is the review `/ship` runs.

1. Read the list of findings. Did it find all three bugs? (Answers are at the bottom.)
2. Tell it which findings to fix.
3. **Run the same review one more time on the fixed code**, and read the new list.

## What happened in my run (25 November 2026)

- The review took 53 seconds. It found all three hidden bugs, and a fourth real bug that I had not planted.
- It did not change my files by itself. It gave me the list and waited. In my run `/ship` started in its review-only mode, because GitHub CLI was not signed in yet in that terminal. Per Anthropic's docs the full `/ship` can also commit, push and open the pull request for you, and merging always stays with you.
- I told it to fix six findings. It did, and all tests passed.
- Then I ran the same review again on the fixed code. It still listed six bugs. Some of them the first review had marked as minor, and one it had called harmless: typing a single `%` into the customer search returned every customer with their email.

So one clean-looking review does not mean the code is safe. Anthropic says the same in its docs: "Claude Ship uses AI and may miss bugs, security vulnerabilities, or other issues."

## The three hidden bugs (spoilers)

<details>
<summary>Show the answers</summary>

1. **Money:** `order_total` applies a discount code twice. With `WELCOME10`, goods for 100.00 cost 81.00 instead of 90.00.
2. **Data leak:** `find_customers` builds the SQL from the search text (SQL injection). Searching for `' OR '1'='1` returns every customer.
3. **Crash on a date:** `invoice_due` breaks for every order placed in December (month 13), and on days that the next month does not have (for example 31 January).

The fourth bug that the review found on its own: `place_order` saved the order before it computed the due date, so a crash on the date left a saved order behind.

</details>

## Notes

- Claude Ship is in beta and Anthropic's docs change. I checked everything above on 25 November 2026.
- Your result can differ from mine. A review is not the same on every run, and that is the point of running it twice.
- MIT license. Made for the reel on [@aipractically](https://www.instagram.com/aipractically/).
