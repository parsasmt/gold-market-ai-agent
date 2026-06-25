from agent import GoldMarketAgent


def main():

    print("=" * 60)
    print("        Gold Market AI Agent")
    print("=" * 60)
    print("Ask questions about the gold market.")
    print("Type 'exit' to quit.")
    print("=" * 60)

    # Create agent
    agent = GoldMarketAgent()

    while True:

        # Get user question
        question = input("\nYour question: ")

        # Exit condition
        if question.lower() in ["exit", "quit"]:
            print("\nGoodbye!")
            break

        print("\nAnalyzing market...\n")

        # Generate answer
        answer = agent.run(question)

        print("=" * 60)
        print(answer)
        print("=" * 60)


if __name__ == "__main__":
    main()