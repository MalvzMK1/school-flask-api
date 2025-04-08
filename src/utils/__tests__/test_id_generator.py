from src.utils.id_generator import IdGenerator
import unittest

class TestIdGenerator(unittest.TestCase):
  def test_should_generate_sequential_ids(self):
    id_generator = IdGenerator()
    
    first_id = id_generator.generate()
    second_id = id_generator.generate()
    third_id = id_generator.generate()
    
    self.assertEqual(first_id, 1)
    self.assertEqual(second_id, 2)
    self.assertEqual(third_id, 3)
    
  def test_different_instances_should_have_independent_counters(self):
    generator1 = IdGenerator()
    generator2 = IdGenerator()
    
    id1_from_gen1 = generator1.generate()
    id2_from_gen1 = generator1.generate()
    
    id1_from_gen2 = generator2.generate()
    id2_from_gen2 = generator2.generate()
    
    self.assertEqual(id1_from_gen1, 1)
    self.assertEqual(id2_from_gen1, 2)
    self.assertEqual(id1_from_gen2, 1)
    self.assertEqual(id2_from_gen2, 2)

if __name__ == '__main__':
  unittest.main(verbosity=2)