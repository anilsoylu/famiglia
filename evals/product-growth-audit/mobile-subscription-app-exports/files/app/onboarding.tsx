// app/onboarding.tsx (excerpt)
import { useState } from "react";
import { router } from "expo-router";
import { posthog } from "@/lib/analytics";
import { api } from "@/lib/api";

const QUESTIONS = [
  { key: "goal", title: "What's your main goal?", options: ["Health", "Focus", "Learning", "Mindfulness", "Other"] },
  { key: "experience", title: "Have you used a habit tracker before?", options: ["Never", "A few times", "Yes, daily"] },
  { key: "wakeTime", title: "When do you usually wake up?", options: ["Before 6", "6-8", "8-10", "After 10"] },
  { key: "reminderTime", title: "When should we remind you?", options: ["Morning", "Afternoon", "Evening", "No reminders"] },
  { key: "weekStart", title: "Your week starts on", options: ["Monday", "Sunday"] },
];

export default function Onboarding() {
  const [step, setStep] = useState<"account" | number>("account");
  const [answers, setAnswers] = useState<Record<string, string>>({});

  // Step 0: account first. No skip, no "continue as guest".
  if (step === "account") {
    return (
      <SignUpForm
        title="Create your account"
        fields={["email", "password"]}
        onSubmit={async ({ email, password }) => {
          await api.signUp(email, password); // creates the row in users
          setStep(0);
        }}
      />
    );
  }

  const q = QUESTIONS[step];
  return (
    <QuestionScreen
      title={q.title}
      options={q.options}
      progress={`${step + 1} / ${QUESTIONS.length}`}
      onSelect={async (value) => {
        const next = { ...answers, [q.key]: value };
        setAnswers(next);
        if (step < QUESTIONS.length - 1) return setStep(step + 1);
        await api.saveSettings(next); // answers are stored but not used anywhere else yet
        posthog.capture("onboarding_complete");
        // Habit creation happens on the home screen, after the paywall.
        router.replace({ pathname: "/paywall", params: { source: "onboarding" } });
      }}
    />
  );
}
