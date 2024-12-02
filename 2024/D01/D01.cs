using System;
using System.Globalization;
using System.IO;

namespace advent_2024
{
    class D01
    {
        static void Main()
        {
            string text = "";

            try
            {
                // Open the text file using a stream reader.
                using StreamReader reader = new("input");

                // Read the stream as a string.
                text = reader.ReadToEnd();
            }
            catch (IOException e)
            {
                Console.WriteLine("The file could not be read:");
                Console.WriteLine(e.Message);
            }
            
            // Split text string by newline characters
            string[] delimiters = ["\r\n", "\n", "\r"];
            string[] lines = text.Split(delimiters, StringSplitOptions.None);

            List<int> nums1 = [], nums2 = [];

            foreach (string line in lines)
            {
                string[] twoNums = line.Split(" ", 2, System.StringSplitOptions.RemoveEmptyEntries);
                nums1.Add(int.Parse(twoNums[0]));
                nums2.Add(int.Parse(twoNums[1]));
            }

            nums1.Sort();
            nums2.Sort();

            int totalDiffs = 0;

            for (int i = 0; i < nums1.Count; i++)
            {
                totalDiffs += Math.Abs(nums1[i] - nums2[i]);
            }
            Console.WriteLine($"Day 1 part 1: {totalDiffs}");

            Dictionary<int, int> similarityMap = [];
            Dictionary<int, int> similarityMapTotals = [];

            foreach (int num1 in nums1)
            {
                if (similarityMap.TryGetValue(num1, out int value))
                {
                    similarityMapTotals[num1] += value;
                }
                else
                {
                    int countNum1 = 0;
                    foreach (int num2 in nums2)
                    {
                        // this loop can be sped up using a binary search algorithm, but not worth my effort to write.
                        if (num1 == num2){
                            countNum1 += 1;
                        }
                    }
                    int similarity = num1 * countNum1;
                    similarityMap.Add(num1, similarity);
                    similarityMapTotals.Add(num1, similarity);
                }
            }

            int totalSimilarity = 0;
            foreach (int similarity in similarityMapTotals.Values)
            {
                totalSimilarity += similarity;
            }

            Console.WriteLine($"Day 1 part 2: {totalSimilarity}");
        }
    }
}

