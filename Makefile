.PHONY: install run clean

install:               ## install the package + deps (editable)
	pip install -e .

run:                   ## run a decision: make run TICKER=NVDA
	python -m open_tradingagents.main $(TICKER)

clean:
	rm -f trading_memory.sqlite
