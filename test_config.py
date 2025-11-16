"""
Test script to verify shapes_config.py compatibility with tangram_game.py
"""

from shapes_config import get_shape_pieces, get_all_shapes, PIECE_SIZES

print("="*60)
print("Testing shapes_config.py compatibility with tangram_game.py")
print("="*60)

# Test get_all_shapes()
print("\n1. Testing get_all_shapes()...")
all_shapes = get_all_shapes()
print(f"   ✓ Found {len(all_shapes)} shapes: {list(all_shapes.keys())}")

# Test each shape
for shape_name in all_shapes.keys():
    print(f"\n2. Testing shape: '{shape_name}'")
    shape_data = all_shapes[shape_name]
    
    # Check structure
    assert 'name' in shape_data, f"Missing 'name' in {shape_name}"
    assert 'difficulty' in shape_data, f"Missing 'difficulty' in {shape_name}"
    assert 'pieces' in shape_data, f"Missing 'pieces' in {shape_name}"
    
    print(f"   ✓ Name: {shape_data['name']}")
    print(f"   ✓ Difficulty: {shape_data['difficulty']}")
    print(f"   ✓ Pieces count: {len(shape_data['pieces'])}")
    
    # Test get_shape_pieces()
    pieces = get_shape_pieces(shape_name)
    print(f"   ✓ get_shape_pieces() returned {len(pieces)} pieces")
    
    # Validate each piece
    for i, piece in enumerate(pieces):
        assert 'color' in piece, f"Missing 'color' in piece {i}"
        assert 'center' in piece, f"Missing 'center' in piece {i}"
        assert 'angle' in piece, f"Missing 'angle' in piece {i}"
        assert 'piece_type' in piece, f"Missing 'piece_type' in piece {i}"
        
        # Validate piece_type is in PIECE_SIZES
        assert piece['piece_type'] in PIECE_SIZES, f"Unknown piece_type: {piece['piece_type']}"
    
    print(f"   ✓ All pieces validated")

# Test PIECE_SIZES
print(f"\n3. Testing PIECE_SIZES...")
print(f"   ✓ PIECE_SIZES has {len(PIECE_SIZES)} entries")
for piece_type, size in PIECE_SIZES.items():
    print(f"   - {piece_type}: {size}px")

print("\n" + "="*60)
print("✅ ALL TESTS PASSED!")
print("shapes_config.py is fully compatible with tangram_game.py")
print("="*60)
